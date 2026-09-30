"""Kenyan-themed design system — color palette, persona colors, and CSS injection."""

import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# Kenyan Flag Color Palette
# ──────────────────────────────────────────────────────────────────────────────
KENYAN_GREEN = "#006600"
KENYAN_RED = "#BB0000"
KENYAN_BLACK = "#111111"
KENYAN_GOLD = "#D4AF37"
KENYAN_WHITE = "#F8F9FA"

# Persona → color mapping used across all charts and cards
PERSONA_COLORS = {
    "Champions": KENYAN_GREEN,
    "Loyal Customers": "#2196F3",
    "At-Risk": KENYAN_GOLD,
    "Lost": KENYAN_RED,
}

# Persona → emoji mapping for UI cards
PERSONA_EMOJIS = {
    "Champions": "🏆",
    "Loyal Customers": "💎",
    "At-Risk": "⚠️",
    "Lost": "🚨",
}

# Persona descriptions for narrative cards
PERSONA_DESCRIPTIONS = {
    "Champions": (
        "Bought recently, buy often, and spend the most. These are our VIP "
        "customers who drive the highest lifetime value. They are brand advocates "
        "and deserve early access to new products, exclusive loyalty rewards, and "
        "personalised engagement."
    ),
    "Loyal Customers": (
        "Consistent buyers with strong spending habits. They may not reach "
        "Champion-level frequency, but their steady patronage forms the backbone "
        "of predictable revenue. Cross-selling and referral programs can elevate "
        "them to Champion status."
    ),
    "At-Risk": (
        "Previously active customers showing signs of disengagement — their "
        "recency is climbing while frequency has declined. Urgent win-back "
        "campaigns, personalised discounts via SMS or WhatsApp, and feedback "
        "surveys are critical to prevent full churn."
    ),
    "Lost": (
        "Customers who haven't purchased in a long time, often with low "
        "historical frequency and spend. While re-acquisition is possible, "
        "the cost is high. Focus on low-cost automated email campaigns and "
        "avoid heavy promotional spend on this segment."
    ),
}


def inject_custom_css() -> None:
    """Inject custom CSS to hide Streamlit chrome and apply Kenyan storyboard styling."""
    st.markdown(
        """
<style>
/* Hide default Streamlit chrome */
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton {
    display: none !important;
}

/* Narrative section styling */
.storyboard-section {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.section-header {
    font-size: 1.8rem;
    font-weight: 700;
    color: #111111;
    border-bottom: 3px solid #006600;
    padding-bottom: 0.5rem;
    margin-bottom: 1.2rem;
}

.section-subtitle {
    font-size: 1.1rem;
    color: #6B7280;
    font-style: italic;
    margin-bottom: 1rem;
}

.persona-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
    border-left: 5px solid;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

.brand-banner {
    background: linear-gradient(135deg, #006600 0%, #004400 100%);
    color: white;
    padding: 2.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
}

.brand-banner h1 {
    font-size: 2.5rem;
    margin: 0;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.brand-banner p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-top: 0.5rem;
}
</style>
""",
        unsafe_allow_html=True,
    )
