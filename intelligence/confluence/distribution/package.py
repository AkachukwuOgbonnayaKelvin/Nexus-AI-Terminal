"""
Phase 6: Distribution API - Confluence Intelligence Package

Internal object that collects all completed Phase 5 intelligence.
This is NOT sent to downstream systems directly.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..contracts import (
    GlobalEntityRating,
    AssetClassRating,
    HarmonizedResult,
    GlobalRisk,
    GlobalTheme,
)


@dataclass
class ConfluenceIntelligencePackage:
    """
    Internal package containing all completed Confluence intelligence.

    This is the internal representation of all Phase 4 and Phase 5 outputs.
    It is used as input to the Distribution API builders.
    """

    # Entity Intelligence (Phase 4)
    entity_ratings: List[GlobalEntityRating] = field(default_factory=list)

    # Asset-Class Intelligence (Phase 5)
    asset_class_ratings: List[AssetClassRating] = field(default_factory=list)

    # Harmonized Results (Phase 3) - for evidence tracking
    harmonized_results: List[HarmonizedResult] = field(default_factory=list)

    # Global State
    global_regime: str = "UNKNOWN"
    global_regime_confidence: float = 0.0
    global_risk_level: str = "UNKNOWN"
    global_risk_score: float = 0.0

    # Drivers & Risks
    key_drivers: List[str] = field(default_factory=list)
    global_risks: List[GlobalRisk] = field(default_factory=list)

    # Themes
    global_themes: List[GlobalTheme] = field(default_factory=list)

    # Opportunities
    top_opportunities: List[Dict[str, Any]] = field(default_factory=list)

    # Metadata
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"

    @property
    def currency_ratings(self) -> List[GlobalEntityRating]:
        """Get only currency entity ratings."""
        from ..entity.classifier import EntityClassifier

        return [
            r for r in self.entity_ratings if EntityClassifier.is_currency(r.entity)
        ]

    @property
    def commodity_ratings(self) -> List[GlobalEntityRating]:
        """Get only commodity entity ratings."""
        from ..entity.classifier import EntityClassifier

        return [
            r for r in self.entity_ratings if EntityClassifier.is_commodity(r.entity)
        ]

    @property
    def index_ratings(self) -> List[GlobalEntityRating]:
        """Get only index entity ratings."""
        from ..entity.classifier import EntityClassifier

        return [r for r in self.entity_ratings if EntityClassifier.is_index(r.entity)]

    @property
    def bond_ratings(self) -> List[GlobalEntityRating]:
        """Get only bond entity ratings."""
        from ..entity.classifier import EntityClassifier

        return [r for r in self.entity_ratings if EntityClassifier.is_bond(r.entity)]

    @property
    def strongest_currency(self) -> Optional[GlobalEntityRating]:
        """Get the strongest currency by score."""
        if not self.currency_ratings:
            return None
        return max(self.currency_ratings, key=lambda r: r.score)

    @property
    def weakest_currency(self) -> Optional[GlobalEntityRating]:
        """Get the weakest currency by score."""
        if not self.currency_ratings:
            return None
        return min(self.currency_ratings, key=lambda r: r.score)

    @property
    def strongest_asset_class(self) -> Optional[AssetClassRating]:
        """Get the strongest asset class by score."""
        if not self.asset_class_ratings:
            return None
        return max(self.asset_class_ratings, key=lambda r: r.score)

    @property
    def weakest_asset_class(self) -> Optional[AssetClassRating]:
        """Get the weakest asset class by score."""
        if not self.asset_class_ratings:
            return None
        return min(self.asset_class_ratings, key=lambda r: r.score)

    def has_entity(self, entity: str) -> bool:
        """Check if an entity exists in the package."""
        return any(r.entity == entity for r in self.entity_ratings)

    def get_entity_rating(self, entity: str) -> Optional[GlobalEntityRating]:
        """Get rating for a specific entity."""
        for r in self.entity_ratings:
            if r.entity == entity:
                return r
        return None

    def __repr__(self) -> str:
        return (
            f"ConfluenceIntelligencePackage("
            f"entities={len(self.entity_ratings)}, "
            f"asset_classes={len(self.asset_class_ratings)}, "
            f"regime={self.global_regime})"
        )
