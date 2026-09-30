"""
Synthetic Data Generator
========================
Generates 5,000 e-commerce transaction records for a hypothetical Kenyan
retailer. Uses fixed random seeds for full reproducibility, seasonal date
weighting to simulate realistic purchase patterns, and log-normal pricing
per product category in Kenyan Shillings (KES).
"""

import numpy as np
import pandas as pd
import streamlit as st

from config.settings import (
    CATEGORIES,
    CATEGORY_PRICE_PARAMS,
    CATEGORY_PROBS,
    DATA_END_DATE,
    DATA_SPAN_DAYS,
    N_CUSTOMERS,
    N_RECORDS,
    RANDOM_SEED,
    REGION_PROBS,
    REGIONS,
)


@st.cache_data(show_spinner=False)
def generate_synthetic_data(
    n_records: int = N_RECORDS,
    n_customers: int = N_CUSTOMERS,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Generate synthetic e-commerce transactions for a Kenyan retailer.

    Parameters
    ----------
    n_records : int
        Total number of transaction rows to generate (default 5,000).
    n_customers : int
        Size of the customer ID pool (default 1,000).
    seed : int
        Random seed for reproducibility (default 42).

    Returns
    -------
    pd.DataFrame
        Transaction-level DataFrame sorted by date with columns:
        TransactionID, CustomerID, TransactionDate, TransactionAmount,
        ProductCategory, Region.
    """
    np.random.seed(seed)

    # ── Customer pool ────────────────────────────────────────────────────
    # Power-law (Dirichlet α=0.5) sampling simulates realistic e-commerce
    # repeat-buyer distribution: top 20% of customers drive ~50% of orders.
    customer_ids = [f"CUST-{i:04d}" for i in range(1, n_customers + 1)]
    weights = np.random.dirichlet(np.ones(n_customers) * 0.5)
    sampled_customers = np.random.choice(customer_ids, size=n_records, p=weights)

    # ── Transaction IDs ──────────────────────────────────────────────────
    transaction_ids = [f"TXN-{i:05d}" for i in range(1, n_records + 1)]

    # ── Dates with seasonal weighting ────────────────────────────────────
    end_date = pd.Timestamp(DATA_END_DATE)
    start_date = end_date - pd.Timedelta(days=DATA_SPAN_DAYS)
    all_dates = pd.date_range(start=start_date, end=end_date, freq="D")

    date_weights = _build_seasonal_weights(all_dates)
    sampled_dates = np.random.choice(all_dates, size=n_records, p=date_weights)

    # ── Product categories ───────────────────────────────────────────────
    sampled_categories = np.random.choice(
        CATEGORIES, size=n_records, p=CATEGORY_PROBS
    )

    # ── Regions ──────────────────────────────────────────────────────────
    sampled_regions = np.random.choice(REGIONS, size=n_records, p=REGION_PROBS)

    # ── Transaction amounts (KES) ────────────────────────────────────────
    amounts = _generate_amounts(sampled_categories, n_records)

    df = pd.DataFrame(
        {
            "TransactionID": transaction_ids,
            "CustomerID": sampled_customers,
            "TransactionDate": pd.to_datetime(sampled_dates),
            "TransactionAmount": amounts,
            "ProductCategory": sampled_categories,
            "Region": sampled_regions,
        }
    )
    return df.sort_values("TransactionDate").reset_index(drop=True)


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────


def _build_seasonal_weights(dates: pd.DatetimeIndex) -> np.ndarray:
    """Build a probability vector with Kenyan seasonal commerce spikes.

    Spikes applied:
    - Q4 Holiday & Jamhuri Day (Nov 15 – Dec 31): 2.0× baseline
    - Easter & Back-to-School (April, August): 1.3× baseline
    - Month-end payday (days 27–31): 1.4× baseline
    """
    weights = np.ones(len(dates))
    for i, d in enumerate(dates):
        if d.month == 12 or (d.month == 11 and d.day >= 15):
            weights[i] *= 2.0
        if d.month in (4, 8):
            weights[i] *= 1.3
        if d.day >= 27:
            weights[i] *= 1.4
    weights /= weights.sum()
    return weights


def _generate_amounts(categories: np.ndarray, n: int) -> np.ndarray:
    """Generate log-normal transaction amounts (KES) per product category."""
    amounts = np.zeros(n)
    for i in range(n):
        params = CATEGORY_PRICE_PARAMS[categories[i]]
        mu = np.log(params["mean"]) - 0.5
        amt = np.random.lognormal(mean=mu, sigma=0.6)
        amounts[i] = round(np.clip(amt, params["min"], params["max"]), 2)
    return amounts
