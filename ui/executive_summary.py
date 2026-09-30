"""Section 1 — Executive Summary: 'Customer Retention & Value Analysis'."""

import pandas as pd
import streamlit as st

from utils.formatting import format_kes


def render_executive_summary(df: pd.DataFrame, rfm: pd.DataFrame) -> None:
    """Render the executive summary section with KPI metrics and narrative.

    Parameters
    ----------
    df : pd.DataFrame
        Raw transaction-level data.
    rfm : pd.DataFrame
        Customer-level RFM data with Persona column.
    """
    total_revenue = df["TransactionAmount"].sum()
    active_customers = df["CustomerID"].nunique()
    avg_order_value = df["TransactionAmount"].mean()
    total_transactions = len(df)

    # Section heading
    st.markdown(
        '<div class="section-header">📊 Customer Retention & Value Analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        "Executive Summary — Understanding Our Customer Base"
        "</div>",
        unsafe_allow_html=True,
    )

    # KPI metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Revenue",
            value=format_kes(total_revenue),
            delta=f"{total_transactions:,} transactions",
        )
    with col2:
        st.metric(
            label="Active Customers",
            value=f"{active_customers:,}",
            delta="Unique buyers in 12 months",
        )
    with col3:
        st.metric(
            label="Average Order Value",
            value=format_kes(avg_order_value),
            delta=f"{total_revenue / active_customers:,.0f} KES per customer",
        )

    st.markdown("---")

    # Narrative diagnosis
    champions_pct = len(rfm[rfm["Persona"] == "Champions"]) / len(rfm) * 100
    at_risk_count = len(rfm[rfm["Persona"] == "At-Risk"])
    at_risk_pct = at_risk_count / len(rfm) * 100
    lost_count = len(rfm[rfm["Persona"] == "Lost"])

    st.markdown(
        f"""
Over the past 12 months, our Kenyan e-commerce platform processed
**{total_transactions:,} transactions** generating **{format_kes(total_revenue)}**
in total revenue across **{active_customers:,} unique customers**.

However, our customer base tells a deeper story. While **{champions_pct:.0f}%** of
customers are **Champions** — our most valuable repeat buyers — a concerning
**{at_risk_pct:.0f}%** fall into the **At-Risk** category, meaning they were once
active but are now showing signs of disengagement. Another **{lost_count:,}**
customers appear to be **Lost** entirely.

This storyboard explores the data behind these segments, identifies where revenue
is concentrated, and proposes targeted interventions to protect and grow our
customer base.
"""
    )

    st.markdown("<br>", unsafe_allow_html=True)
