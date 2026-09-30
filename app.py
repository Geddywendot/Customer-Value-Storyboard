"""
Customer Value Storyboard — Entry Point
========================================
A production-quality Streamlit application serving as an interactive
"Data Storyboard" for Customer Segmentation, targeting a hypothetical
Kenyan e-commerce retailer.

Run with:
    streamlit run app.py
"""

import streamlit as st  # type: ignore[import-not-found]

# ──────────────────────────────────────────────────────────────────────────────
# Page Configuration — MUST be the first Streamlit command
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Value Storyboard",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────────
# Imports (after page config to satisfy Streamlit ordering constraint)
# ──────────────────────────────────────────────────────────────────────────────
from analysis.rfm import calculate_rfm_and_clusters  # noqa: E402
from config.theme import inject_custom_css  # noqa: E402
from data.generator import generate_synthetic_data  # noqa: E402
from ui.banner import render_banner  # noqa: E402
from ui.churn_risk import render_churn_risk  # noqa: E402
from ui.executive_summary import render_executive_summary  # noqa: E402
from ui.revenue import render_revenue_concentration  # noqa: E402
from ui.segmentation import render_segmentation  # noqa: E402


def main() -> None:
    """Orchestrate the storyboard: load data, inject styles, render sections."""
    # Apply Kenyan design system
    inject_custom_css()

    # Load data (cached — instantaneous on rerun)
    df = generate_synthetic_data()
    rfm = calculate_rfm_and_clusters(df)

    # Render narrative storyboard sections in scrolling order
    render_banner()
    render_executive_summary(df, rfm)
    render_revenue_concentration(df)
    render_segmentation(rfm)
    render_churn_risk(df, rfm)


if __name__ == "__main__":
    main()
else:
    # Streamlit runs the module directly (not via __main__),
    # so we call main() unconditionally when the module is loaded.
    main()
