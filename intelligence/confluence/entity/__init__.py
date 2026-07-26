"""
Phase 4: Global Entity Intelligence

The Global Entity Intelligence phase converts harmonized results
into complete entity ratings for:
- Currencies
- Indices
- Commodities
- Bonds/Rates
"""

from .aggregator import EntityAggregator
from .classifier import EntityClassifier
from .direction import classify_direction, is_bearish, is_bullish, is_neutral
from .ranker import EntityRanker
from .rating_engine import EntityRatingEngine

__all__ = [
    "EntityAggregator",
    "EntityClassifier",
    "EntityRanker",
    "EntityRatingEngine",
    "classify_direction",
    "is_bearish",
    "is_bullish",
    "is_neutral",
]
