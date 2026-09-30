"""Application-wide constants and configuration settings."""

# Data generation parameters
N_RECORDS = 5000
N_CUSTOMERS = 1000
RANDOM_SEED = 42

# Clustering parameters
N_CLUSTERS = 4
KMEANS_N_INIT = 10
KMEANS_MAX_ITER = 300

# Persona labels — ordered from highest value to lowest
PERSONA_ORDER = ["Champions", "Loyal Customers", "At-Risk", "Lost"]

# Product categories with market share probabilities
CATEGORIES = ["Groceries", "Fashion", "Home", "Electronics"]
CATEGORY_PROBS = [0.35, 0.25, 0.20, 0.20]

# Category pricing tiers (KES)
CATEGORY_PRICE_PARAMS = {
    "Electronics": {"mean": 18500, "min": 3500, "max": 85000},
    "Groceries": {"mean": 2400, "min": 350, "max": 9000},
    "Fashion": {"mean": 4800, "min": 1000, "max": 18000},
    "Home": {"mean": 8500, "min": 1500, "max": 35000},
}

# Kenyan regions with commerce concentration probabilities
REGIONS = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
REGION_PROBS = [0.46, 0.20, 0.14, 0.12, 0.08]

# Date anchor for synthetic data
DATA_END_DATE = "2026-09-30"
DATA_SPAN_DAYS = 365
