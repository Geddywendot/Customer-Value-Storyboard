"""
RFM Analysis & K-Means Clustering
==================================
Calculates Recency, Frequency, and Monetary metrics per customer, applies
StandardScaler + KMeans(n_clusters=4), and deterministically maps clusters
to business personas by sorting centroids on Monetary spend.
"""

import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from config.settings import (
    KMEANS_MAX_ITER,
    KMEANS_N_INIT,
    N_CLUSTERS,
    PERSONA_ORDER,
    RANDOM_SEED,
)


@st.cache_data(show_spinner=False)
def calculate_rfm_and_clusters(
    df: pd.DataFrame, random_state: int = RANDOM_SEED
) -> pd.DataFrame:
    """Calculate RFM metrics and assign deterministic customer personas.

    Parameters
    ----------
    df : pd.DataFrame
        Transaction-level data with at least CustomerID, TransactionDate,
        TransactionID, and TransactionAmount columns.
    random_state : int
        Seed for KMeans reproducibility (default 42).

    Returns
    -------
    pd.DataFrame
        Customer-level DataFrame with Recency, Frequency, Monetary,
        Cluster, and Persona columns.
    """

    # 1. RFM (Recency, Frequency, Monetary) is selected as the industry
    # standard behavioral segmentation framework for e-commerce, capturing
    # how recently, how often, and how much customers spend.

    # 2. Establish a reference snapshot date one day past the latest
    # transaction to calculate customer recency deterministically without
    # temporal leakage or zero-day division errors.
    snapshot_date = df["TransactionDate"].max() + pd.Timedelta(days=1)

    # 3. Aggregate customer transactions: Recency measures days since last
    # order, Frequency counts total orders, and Monetary computes total
    # lifetime transaction value in Kenyan Shillings (KES).
    rfm = (
        df.groupby("CustomerID")
        .agg(
            Recency=("TransactionDate", lambda x: (snapshot_date - x.max()).days),
            Frequency=("TransactionID", "count"),
            Monetary=("TransactionAmount", "sum"),
        )
        .reset_index()
    )

    # 4. Standardize RFM features using StandardScaler to eliminate scale
    # disparity: Monetary (KES tens of thousands) would otherwise overwhelm
    # Recency (days) and Frequency (counts) in Euclidean distance calculations.
    scaler = StandardScaler()

    # 5. StandardScaler applies zero-mean, unit-variance transformation
    # (z = (x - mu) / sigma), guaranteeing that each RFM dimension exerts
    # equal weight during iterative centroid convergence.
    rfm_features = rfm[["Recency", "Frequency", "Monetary"]]
    rfm_scaled = scaler.fit_transform(rfm_features)

    # 6. Initialize KMeans with exactly 4 clusters, k-means++ centroid
    # seeding to accelerate convergence, and n_init=10 to evaluate multiple
    # starting positions and avoid local inertia minima.
    kmeans = KMeans(
        n_clusters=N_CLUSTERS,
        init="k-means++",
        n_init=KMEANS_N_INIT,
        max_iter=KMEANS_MAX_ITER,
        random_state=random_state,
    )

    # 7. Fix random_state=42 across scikit-learn and numpy to ensure strict
    # mathematical reproducibility across diverse execution environments
    # and client sessions.
    rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

    # 8. Compute unscaled cluster profile means (Recency, Frequency,
    # Monetary) to inspect and interpret empirical behavioral differences
    # across each identified customer group.
    cluster_profiles = rfm.groupby("Cluster")[
        ["Recency", "Frequency", "Monetary"]
    ].mean()

    # 9. Critical: Programmatically sort cluster centroids by Monetary
    # spend before assigning persona labels, preventing arbitrary cluster
    # ID assignment (label flipping) inherent to unsupervised K-Means.
    sorted_cluster_ids = cluster_profiles.sort_values(
        by="Monetary", ascending=False
    ).index.tolist()

    # 10. Map sorted cluster indices monotonically to business personas:
    # Rank 0 -> 'Champions' (highest value), Rank 1 -> 'Loyal Customers',
    # Rank 2 -> 'At-Risk' (churn danger), Rank 3 -> 'Lost' (lowest engagement).
    cluster_to_persona = dict(zip(sorted_cluster_ids, PERSONA_ORDER))
    rfm["Persona"] = rfm["Cluster"].map(cluster_to_persona)

    return rfm
