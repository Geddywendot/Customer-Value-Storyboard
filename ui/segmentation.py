"""Section 3 — Customer Segmentation: 'The Core Analysis'."""

import pandas as pd
import plotly.express as px
import streamlit as st

from config.theme import (
    KENYAN_BLACK,
    KENYAN_WHITE,
    PERSONA_COLORS,
    PERSONA_DESCRIPTIONS,
    PERSONA_EMOJIS,
)
from utils.formatting import format_kes


def render_segmentation(rfm: pd.DataFrame) -> None:
    """Render the segmentation section with 3D scatter, persona cards, and table.

    Parameters
    ----------
    rfm : pd.DataFrame
        Customer-level RFM data with Persona column.
    """
    st.markdown(
        '<div class="section-header">🔬 Customer Segmentation</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">'
        "The Core Analysis — Who Are Our Customers?"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
Using **RFM Analysis** (Recency, Frequency, Monetary) combined with **K-Means
clustering**, we segmented our customer base into four distinct personas. The 3D
scatter plot below visualises each customer positioned by how **recently** they
purchased (Recency), how **often** they buy (Frequency), and how **much** they
spend (Monetary value in KES).
"""
    )

    # ── 3D Scatter Plot ──────────────────────────────────────────────────
    _render_3d_scatter(rfm)

    # ── Persona cards ────────────────────────────────────────────────────
    st.markdown("### Customer Personas")
    _render_persona_cards(rfm)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary table ────────────────────────────────────────────────────
    st.markdown("### Segment Summary Table")
    _render_summary_table(rfm)

    st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Private helpers
# ──────────────────────────────────────────────────────────────────────────────


def _render_3d_scatter(rfm: pd.DataFrame) -> None:
    """Render the 3D Plotly scatter plot colour-coded by persona."""
    fig = px.scatter_3d(
        rfm,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Persona",
        color_discrete_map=PERSONA_COLORS,
        title="Customer Segments: Recency × Frequency × Monetary (KES)",
        labels={
            "Recency": "Recency (days)",
            "Frequency": "Frequency (orders)",
            "Monetary": "Monetary (KES)",
        },
        opacity=0.75,
        hover_data={
            "CustomerID": True,
            "Recency": True,
            "Frequency": True,
            "Monetary": ":.2f",
        },
    )
    fig.update_layout(
        font=dict(family="Inter, sans-serif", size=12),
        title_font_size=18,
        title_font_color=KENYAN_BLACK,
        height=600,
        scene=dict(
            xaxis_title="Recency (days since last order)",
            yaxis_title="Frequency (total orders)",
            zaxis_title="Monetary (KES total spend)",
            bgcolor=KENYAN_WHITE,
        ),
        legend=dict(
            title="Customer Persona",
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E5E7EB",
            borderwidth=1,
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_persona_cards(rfm: pd.DataFrame) -> None:
    """Render styled HTML cards for each persona with stats."""
    for persona, desc in PERSONA_DESCRIPTIONS.items():
        count = len(rfm[rfm["Persona"] == persona])
        pct = count / len(rfm) * 100
        avg_monetary = rfm[rfm["Persona"] == persona]["Monetary"].mean()
        emoji = PERSONA_EMOJIS[persona]
        color = PERSONA_COLORS[persona]

        st.markdown(
            f"""
<div class="persona-card" style="border-left-color: {color}">
    <strong>{emoji} {persona}</strong> — {count:,} customers ({pct:.1f}%)
    | Avg. Spend: {format_kes(avg_monetary)}<br>
    <span style="color: #4B5563">{desc}</span>
</div>
""",
            unsafe_allow_html=True,
        )


def _render_summary_table(rfm: pd.DataFrame) -> None:
    """Render the cluster summary DataFrame with hidden index."""
    summary = (
        rfm.groupby("Persona")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean"),
            Total_Revenue=("Monetary", "sum"),
        )
        .reset_index()
    )
    summary["Avg_Recency"] = summary["Avg_Recency"].round(1)
    summary["Avg_Frequency"] = summary["Avg_Frequency"].round(1)
    summary["Avg_Monetary"] = summary["Avg_Monetary"].round(2)
    summary["Total_Revenue"] = summary["Total_Revenue"].round(2)
    summary.columns = [
        "Persona",
        "Customers",
        "Avg Recency (days)",
        "Avg Frequency (orders)",
        "Avg Monetary (KES)",
        "Total Revenue (KES)",
    ]

    st.dataframe(
        summary.style.format(
            {
                "Avg Monetary (KES)": "{:,.2f}",
                "Total Revenue (KES)": "{:,.2f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )
