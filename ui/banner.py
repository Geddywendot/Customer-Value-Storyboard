"""Brand banner rendered at the top of the storyboard."""

import streamlit as st


def render_banner() -> None:
    """Render the Kenyan-themed brand banner with app title and subtitle."""
    st.markdown(
        """
<div class="brand-banner">
    <h1>🇰🇪 Customer Value Storyboard</h1>
    <p>Data-Driven Customer Segmentation for a Kenyan E-Commerce Retailer</p>
</div>
""",
        unsafe_allow_html=True,
    )
