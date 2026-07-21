"""
GLB-003 Macro Intelligence Engine - Constants
"""

# NDIP Topics
NDIP_TOPICS = {
    "GDP": "macro.statistics.gdp",
    "CPI": "macro.statistics.cpi",
    "EMPLOYMENT": "macro.statistics.employment",
    "PMI": "macro.statistics.pmi",
}

# Weights for macro components
COMPONENT_WEIGHTS = {
    "growth": 0.30,
    "inflation": 0.25,
    "employment": 0.25,
    "pmi": 0.20,
}
