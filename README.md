# Customer Value Storyboard

An interactive "Data Storyboard" built with Streamlit for Customer Segmentation. This application generates synthetic transaction data for a hypothetical Kenyan e-commerce retailer, performs RFM (Recency, Frequency, Monetary) analysis, applies K-Means clustering, and displays the results in a narrative-driven scrolling format.

## Features

1. **Synthetic Data Generation**: 
   - 5,000 transaction records for ~1,000 unique customers over 12 months.
   - Realistic seasonal purchasing patterns (e.g., spikes during Black Friday and Easter).
   - Right-skewed spending distributions across product categories.

2. **RFM Analysis & Deterministic Clustering**: 
   - Calculates Recency, Frequency, and Monetary metrics per customer.
   - Groups customers into 4 distinct segments using K-Means clustering.
   - Dynamically and deterministically maps cluster centroids to actionable personas: **Champions**, **Loyal Customers**, **At-Risk**, and **Lost**.

3. **Narrative UI Layout**:
   - **Executive Summary**: High-level KPIs and business context.
   - **Revenue Concentration**: Treemap breakdown by Region and Category.
   - **Segmentation**: 3D interactive scatter plot of the RFM clusters.
   - **Churn Risk**: Risk analysis with strategic, persona-specific interventions.

## Setup and Installation

Requires Python 3.8+

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd Customer-Value-Storyboard
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

## Tech Stack
- **Streamlit**: Web application framework
- **Pandas & NumPy**: Data generation and manipulation
- **Scikit-Learn**: Machine learning (StandardScaler, KMeans)
- **Plotly Express**: Interactive data visualizations
