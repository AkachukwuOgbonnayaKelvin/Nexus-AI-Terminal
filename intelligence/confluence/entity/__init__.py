"""
Phase 4: Global Entity Intelligence

The Global Entity Intelligence phase converts harmonized results
into complete entity ratings for:
- Currencies
- Indices
- Commodities
- Bonds/Rates
"""

from .classifier import EntityClassifier
from .aggregator import EntityAggregator
from .rating_engine import EntityRatingEngine
from .ranker import EntityRanker
from .direction import classify_direction, is_bullish, is_bearish, is_neutral

__all__ = [
    "EntityClassifier",
    "EntityAggregator",
    "EntityRatingEngine",
    "EntityRanker",
    "classify_direction",
    "is_bullish",
    "is_bearish",
    "is_neutral",
]
