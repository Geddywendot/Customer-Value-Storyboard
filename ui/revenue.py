"""Section 2 — Revenue Concentration: 'The Problem'."""

import pandas as pd
import plotly.express as px
import streamlit as st

from config.theme import KENYAN_BLACK, KENYAN_GOLD, KENYAN_GREEN, KENYAN_RED


def render_revenue_concentration(df: pd.DataFrame) -> None:
    """Render the revenue concentration section with treemap and narrative.

    Parameters
    ----------
    df : pd.DataFrame
        Raw transaction-level data.
    """
    total_revenue = df["TransactionAmount"].sum()

    st.markdown(
        '<div class="section-header">🗺️ Revenue Concentration</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        "The Problem — Where Our Revenue Comes From"
        "</div>",
        unsafe_allow_html=True,
    )

    # Treemap: revenue by Region → Category
    revenue_breakdown = (
        df.groupby(["Region", "ProductCategory"])["TransactionAmount"]
        .sum()
        .reset_index()
    )
    revenue_breakdown.columns = ["Region", "Category", "Revenue"]

    fig = px.treemap(
        revenue_breakdown,
        path=["Region", "Category"],
        values="Revenue",
        color="Revenue",
        color_continuous_scale=[KENYAN_GREEN, KENYAN_GOLD, KENYAN_RED],
        title="Revenue Distribution by Region & Product Category",
    )
    fig.update_layout(
        font=dict(family="Inter, sans-serif", size=13),
        title_font_size=18,
        title_font_color=KENYAN_BLACK,
        margin=dict(t=50, l=10, r=10, b=10),
        height=500,
    )
    fig.update_traces(
        textinfo="label+value",
        texttemplate="%{label}<br>KES %{value:,.0f}",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Narrative
    nairobi_pct = (
        df[df["Region"] == "Nairobi"]["TransactionAmount"].sum()
        / total_revenue
        * 100
    )
    top_category = (
        df.groupby("ProductCategory")["TransactionAmount"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )
    top_cat_pct = (
        df.groupby("ProductCategory")["TransactionAmount"].sum().max()
        / total_revenue
        * 100
    )

    st.markdown(
        f"""
The treemap above reveals a critical vulnerability: **Nairobi alone accounts for
{nairobi_pct:.1f}% of all revenue** — nearly half of our entire business. While
this reflects Kenya's economic geography, it exposes significant concentration
risk. A disruption in the Nairobi market (logistics issues, competitor entry,
regulatory changes) could disproportionately impact the business.

On the product side, **{top_category}** leads with **{top_cat_pct:.1f}%** of
revenue. Coastal and western regions like Mombasa, Kisumu, Nakuru, and Eldoret
represent untapped growth potential. Understanding *who* our customers are — not
just *where* they shop — is essential. This motivates the segmentation analysis
that follows.
"""
    )

    st.markdown("<br>", unsafe_allow_html=True)
