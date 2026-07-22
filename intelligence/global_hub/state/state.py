"""
Global Intelligence Hub - Canonical State

The single source of truth for the Global Intelligence Dashboard.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from ...confluence.contracts import (
    GlobalEntityRating,
    AssetClassRating,
    GlobalIntelligenceOutput,
)


@dataclass
class GlobalHubState:
    """
    Canonical state for the Global Intelligence Hub.

    This is the single source of truth from which all dashboard
    views are rendered.

    RULE: All required fields (no defaults) must come first.
          All optional fields (with defaults) must come after.
    """

    # ============================================================
    # REQUIRED FIELDS (no defaults) - MUST come first
    # ============================================================

    # Identity
    state_id: str

    # Timestamps
    generated_at: datetime
    valid_until: datetime

    # Global State
    global_regime: str
    global_regime_confidence: float
    global_risk_level: str
    global_risk_score: float

    # Core Intelligence
    global_output: GlobalIntelligenceOutput

    # Rankings
    currency_rankings: List[GlobalEntityRating]
    asset_class_rankings: List[AssetClassRating]
    entity_rankings: List[GlobalEntityRating]

    # Drivers & Risks
    global_drivers: List[str]
    global_risks: List[Dict[str, Any]]
    global_themes: List[Dict[str, Any]]
    top_opportunities: List[Dict[str, Any]]

    # Summaries
    executive_summary: str

    # ============================================================
    # OPTIONAL FIELDS (with defaults) - MUST come after required
    # ============================================================

    schema_version: str = "1.0.0"
    ai_executive_summary: Optional[str] = None
    previous_state_id: Optional[str] = None
    is_valid: bool = True

    # ============================================================
    # METHODS
    # ============================================================

    def get_strongest_currency(self) -> Optional[GlobalEntityRating]:
        if not self.currency_rankings:
            return None
        return self.currency_rankings[0]

    def get_weakest_currency(self) -> Optional[GlobalEntityRating]:
        if not self.currency_rankings:
            return None
        return self.currency_rankings[-1]

    def get_strongest_asset_class(self) -> Optional[AssetClassRating]:
        if not self.asset_class_rankings:
            return None
        return self.asset_class_rankings[0]

    def get_weakest_asset_class(self) -> Optional[AssetClassRating]:
        if not self.asset_class_rankings:
            return None
        return self.asset_class_rankings[-1]

    def is_expired(self) -> bool:
        """Check if the state has expired."""
        return datetime.utcnow() > self.valid_until

    def age_seconds(self) -> float:
        """Get age in seconds since generation."""
        return (datetime.utcnow() - self.generated_at).total_seconds()
