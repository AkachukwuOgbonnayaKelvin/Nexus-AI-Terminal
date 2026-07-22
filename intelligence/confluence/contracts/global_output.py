"""
Confluence Engine - GlobalIntelligenceOutput Contract

Output of Phase 6A: Global Output API.
This is FINAL/POLISHED intelligence for the Global Intelligence Hub.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any

from .entity_rating import GlobalEntityRating
from .asset_class_rating import AssetClassRating


@dataclass
class GlobalTheme:
    """A dominant global theme."""

    name: str
    strength: float  # 0-100
    description: str
    supporting_evidence: List[str] = field(default_factory=list)


@dataclass
class GlobalRisk:
    """A global risk factor."""

    name: str
    severity: float  # 0-100
    description: str
    affected_assets: List[str] = field(default_factory=list)


@dataclass
class GlobalIntelligenceOutput:
    """
    FINAL/POLISHED global intelligence output.

    This goes to the Global Intelligence Hub for display.
    It is complete, organized, and presentation-ready.
    """

    # REQUIRED FIELDS (no defaults)
    global_regime: str
    global_regime_confidence: float
    global_risk_level: str
    global_risk_score: float

    # OPTIONAL FIELDS (with defaults)
    currency_rankings: List[GlobalEntityRating] = field(default_factory=list)
    entity_rankings: List[GlobalEntityRating] = field(default_factory=list)
    asset_class_rankings: List[AssetClassRating] = field(default_factory=list)
    global_drivers: List[str] = field(default_factory=list)
    global_risks: List[GlobalRisk] = field(default_factory=list)
    dominant_themes: List[GlobalTheme] = field(default_factory=list)
    top_opportunities: List[Dict[str, Any]] = field(default_factory=list)
    top_risks: List[Dict[str, Any]] = field(default_factory=list)
    executive_summary: str = ""
    ai_context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"

    def get_strongest_currency(self) -> Optional[GlobalEntityRating]:
        """Get the highest-ranked currency."""
        if not self.currency_rankings:
            return None
        return self.currency_rankings[0]

    def get_weakest_currency(self) -> Optional[GlobalEntityRating]:
        """Get the lowest-ranked currency."""
        if not self.currency_rankings:
            return None
        return self.currency_rankings[-1]

    def get_strongest_asset_class(self) -> Optional[AssetClassRating]:
        """Get the highest-ranked asset class."""
        if not self.asset_class_rankings:
            return None
        return self.asset_class_rankings[0]

    def get_weakest_asset_class(self) -> Optional[AssetClassRating]:
        """Get the lowest-ranked asset class."""
        if not self.asset_class_rankings:
            return None
        return self.asset_class_rankings[-1]

    def __repr__(self) -> str:
        return f"GlobalIntelligenceOutput(regime={self.global_regime}, currencies={len(self.currency_rankings)}, classes={len(self.asset_class_rankings)})"
