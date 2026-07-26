"""
Confluence Engine - Contracts Layer

All data contracts for the Confluence Pipeline.
Every phase speaks the same language.
"""

from .asset_class_rating import AssetClass, AssetClassRating
from .asset_feed import AssetIntelligenceFeed, CurrencyContext, FeedStatus
from .entity_rating import EntityDriver, EntityRisk, GlobalEntityRating
from .evidence import EvidenceQuality, EvidenceRecord
from .global_output import GlobalIntelligenceOutput, GlobalRisk, GlobalTheme
from .harmonized_result import ConflictLevel, HarmonizedResult
from .normalized_signal import Direction, EntityType, NormalizedSignal, SignalType

__all__ = [
    "AssetClass",
    "AssetClassRating",
    "AssetIntelligenceFeed",
    "ConflictLevel",
    "CurrencyContext",
    "Direction",
    "EntityDriver",
    "EntityRisk",
    "EntityType",
    "EvidenceQuality",
    "EvidenceRecord",
    "FeedStatus",
    "GlobalEntityRating",
    "GlobalIntelligenceOutput",
    "GlobalRisk",
    "GlobalTheme",
    "HarmonizedResult",
    "NormalizedSignal",
    "SignalType",
]
