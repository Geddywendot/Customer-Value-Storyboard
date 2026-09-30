"""Section 4 — Churn Risk: 'The Call to Action'."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config.theme import KENYAN_BLACK, KENYAN_WHITE, PERSONA_COLORS
from utils.formatting import format_kes


def render_churn_risk(df: pd.DataFrame, rfm: pd.DataFrame) -> None:
    """Render the churn risk section with bar chart and strategic interventions.

    Parameters
    ----------
    df : pd.DataFrame
        Raw transaction-level data (used for regional stats).
    rfm : pd.DataFrame
        Customer-level RFM data with Persona column.
    """
    st.markdown(
        '<div class="section-header">🚨 Churn Risk & Revenue at Stake</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        "The Call to Action — Protecting Our Revenue"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Bar chart: revenue by persona ────────────────────────────────────
    _render_revenue_bar(rfm)

    # ── Risk narrative ───────────────────────────────────────────────────
    _render_risk_narrative(rfm)

    # ── Strategic interventions ──────────────────────────────────────────
    _render_interventions(df, rfm)

    # ── Footer ───────────────────────────────────────────────────────────
    _render_footer(df)


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────


def _render_revenue_bar(rfm: pd.DataFrame) -> None:
    """Render a Plotly bar chart showing total revenue per persona."""
    rev = (
        rfm.groupby("Persona")["Monetary"]
        .sum()
        .reset_index()
        .rename(columns={"Monetary": "Revenue"})
    )
    colors = [PERSONA_COLORS.get(p, KENYAN_BLACK) for p in rev["Persona"]]

    fig = go.Figure(
        data=[
            go.Bar(
                x=rev["Persona"],
                y=rev["Revenue"],
                marker_color=colors,
                text=[f"KES {v:,.0f}" for v in rev["Revenue"]],
                textposition="outside",
                textfont=dict(size=13, color=KENYAN_BLACK),
            )
        ]
    )
    fig.update_layout(
        title="Total Revenue by Customer Segment — Revenue at Risk",
        title_font_size=18,
        title_font_color=KENYAN_BLACK,
        font=dict(family="Inter, sans-serif", size=13),
        xaxis_title="Customer Persona",
        yaxis_title="Total Revenue (KES)",
        yaxis_tickformat=",",
        height=480,
        plot_bgcolor=KENYAN_WHITE,
        showlegend=False,
        margin=dict(t=60, b=40),
    )
    fig.update_xaxes(tickfont=dict(size=14, color=KENYAN_BLACK))
    st.plotly_chart(fig, use_container_width=True)


def _render_risk_narrative(rfm: pd.DataFrame) -> None:
    """Render the revenue-at-risk narrative paragraph."""
    at_risk_revenue = rfm[rfm["Persona"] == "At-Risk"]["Monetary"].sum()
    lost_revenue = rfm[rfm["Persona"] == "Lost"]["Monetary"].sum()
    combined_risk = at_risk_revenue + lost_revenue
    risk_pct = combined_risk / rfm["Monetary"].sum() * 100

    st.markdown(
        f"""
The bar chart above quantifies the financial stakes of each segment. The
**At-Risk** and **Lost** segments together represent
**{format_kes(combined_risk)}** — approximately **{risk_pct:.1f}%** of total
customer lifetime value. This is revenue that is actively eroding or has
already been lost.

The **At-Risk** segment alone holds **{format_kes(at_risk_revenue)}** in
historical spend from customers who are drifting away. Every day without
intervention increases the probability of permanent churn.
"""
    )


def _render_interventions(df: pd.DataFrame, rfm: pd.DataFrame) -> None:
    """Render the 5 strategic intervention recommendations."""
    at_risk_count = len(rfm[rfm["Persona"] == "At-Risk"])
    nairobi_pct = (
        df[df["Region"] == "Nairobi"]["TransactionAmount"].sum()
        / df["TransactionAmount"].sum()
        * 100
    )

    st.markdown("### 🎯 Strategic Interventions")
    st.markdown(
        f"""
Based on our segmentation analysis, we recommend the following targeted
interventions:

**1. 🟢 Champion Retention Program**
> Launch an exclusive loyalty tier for Champions with early access to sales,
> free delivery, and personalised product recommendations. Target: maintain
> 95%+ retention rate. Champions generate the highest per-customer revenue —
> losing even one is costly.

**2. 🟡 At-Risk Win-Back Campaign**
> Deploy targeted SMS and WhatsApp campaigns to the {at_risk_count:,} At-Risk
> customers with time-limited discount codes (15-20% off). Include a feedback
> survey to understand disengagement reasons. Goal: recover 30%+ of At-Risk
> customers within 60 days.

**3. 🔴 Regional Diversification Strategy**
> Reduce Nairobi dependency (currently {nairobi_pct:.0f}% of revenue) by
> investing in marketing and logistics infrastructure in Mombasa, Kisumu, and
> Nakuru. Partner with local influencers and establish regional distribution
> hubs to capture untapped demand.

**4. 📊 Automated Monitoring & Alerting**
> Implement real-time RFM scoring that automatically flags customers
> transitioning from Loyal to At-Risk status. Trigger automated win-back
> sequences before customers reach the Lost segment. Prevention is
> significantly cheaper than re-acquisition.

**5. 🎁 Category Cross-Sell Engine**
> Analyse purchasing patterns to identify cross-sell opportunities — for
> example, Electronics buyers may be receptive to Home accessories. Implement
> recommendation widgets on the platform and in post-purchase emails to
> increase basket size and frequency.
"""
    )


def _render_footer(df: pd.DataFrame) -> None:
    """Render the page footer."""
    total_txns = len(df)
    active = df["CustomerID"].nunique()

    st.markdown("---")
    st.markdown(
        f"""
<div style="text-align: center; color: #9CA3AF; font-size: 0.85rem;
            padding: 1rem 0;">
    🇰🇪 Customer Value Storyboard | Built with Streamlit & Plotly |
    Synthetic data: {total_txns:,} transactions across {active:,} customers |
    Powered by RFM Analysis & K-Means Clustering
</div>
""",
        unsafe_allow_html=True,
    )
