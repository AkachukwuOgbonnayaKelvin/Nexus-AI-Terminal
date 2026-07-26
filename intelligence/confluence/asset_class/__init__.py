"""
Phase 5: Asset-Class Intelligence

The Asset-Class Intelligence phase converts entity ratings
into asset-class ratings for:
- FX
- Metals
- Equities
- Bonds
- Energy
"""

from .aggregator import AssetClassAggregator
from .mapper import AssetClassMapper
from .ranker import AssetClassRanker
from .rating_engine import AssetClassRatingEngine

__all__ = [
    "AssetClassAggregator",
    "AssetClassMapper",
    "AssetClassRanker",
    "AssetClassRatingEngine",
]
