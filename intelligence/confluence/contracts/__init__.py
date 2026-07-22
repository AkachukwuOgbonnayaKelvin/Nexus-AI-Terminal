"""
Confluence Engine - Contracts Layer

All data contracts for the Confluence Pipeline.
Every phase speaks the same language.
"""

from .normalized_signal import NormalizedSignal, Direction, SignalType, EntityType
from .evidence import EvidenceRecord, EvidenceQuality
from .harmonized_result import HarmonizedResult, ConflictLevel
from .entity_rating import GlobalEntityRating, EntityDriver, EntityRisk
from .asset_class_rating import AssetClassRating, AssetClass
from .global_output import GlobalIntelligenceOutput, GlobalTheme, GlobalRisk
from .asset_feed import AssetIntelligenceFeed, FeedStatus, CurrencyContext

__all__ = [
    "NormalizedSignal",
    "Direction",
    "SignalType",
    "EntityType",
    "EvidenceRecord",
    "EvidenceQuality",
    "HarmonizedResult",
    "ConflictLevel",
    "GlobalEntityRating",
    "EntityDriver",
    "EntityRisk",
    "AssetClassRating",
    "AssetClass",
    "GlobalIntelligenceOutput",
    "GlobalTheme",
    "GlobalRisk",
    "AssetIntelligenceFeed",
    "FeedStatus",
    "CurrencyContext",
]
