"""Nexus Data Integration Platform (NDIP).

NDIP is the single entry point for every external data source used in the platform.
It performs ONLY:
- Collection
- Validation
- Normalization
- Classification
- Warehousing
- Distribution

NDIP does NOT perform market intelligence, analysis, scoring, or predictions.
"""

__version__ = "0.1.0"

__all__ = [
    "core",
    "gateway",
    "validation",
    "normalization",
    "classification",
    "warehouse",
    "distribution",
]
