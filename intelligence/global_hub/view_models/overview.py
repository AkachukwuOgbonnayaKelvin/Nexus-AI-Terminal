"""
Global Intelligence Hub - Overview View Model

GUI-ready data for the Global Intelligence Overview.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from ..state.state import GlobalHubState


@dataclass
class OverviewViewModel:
    """
    View model for the Global Intelligence Overview.

    This is the data the GUI needs for the main overview page.
    """

    # Global State
    regime: str
    regime_confidence: float
    risk_level: str
    risk_score: float

    # Top Entities
    strongest_currency: Optional[Dict[str, Any]]
    weakest_currency: Optional[Dict[str, Any]]
    strongest_asset_class: Optional[Dict[str, Any]]
    weakest_asset_class: Optional[Dict[str, Any]]

    # Rankings (top 5)
    top_currencies: List[Dict[str, Any]]
    top_asset_classes: List[Dict[str, Any]]

    # Drivers & Risks
    top_drivers: List[str]
    top_risks: List[Dict[str, Any]]

    # Summary
    executive_summary: str

    # Timestamps
    generated_at: str
    valid_until: str

    @classmethod
    def from_state(cls, state: GlobalHubState) -> "OverviewViewModel":
        """Create view model from canonical state."""

        # Top currencies
        top_currencies = []
        for c in state.currency_rankings[:5]:
            top_currencies.append(
                {
                    "symbol": c.entity,
                    "score": c.score,
                    "direction": c.direction.value,
                    "confidence": c.confidence,
                    "rank": c.rank,
                }
            )

        # Top asset classes
        top_asset_classes = []
        for a in state.asset_class_rankings[:5]:
            top_asset_classes.append(
                {
                    "name": a.name,
                    "asset_class": a.asset_class.value,
                    "score": a.score,
                    "direction": a.direction.value,
                    "confidence": a.confidence,
                    "rank": a.rank,
                }
            )

        # Strongest/weakest
        strongest_curr = state.get_strongest_currency()
        weakest_curr = state.get_weakest_currency()
        strongest_asset = state.get_strongest_asset_class()
        weakest_asset = state.get_weakest_asset_class()

        return cls(
            regime=state.global_regime,
            regime_confidence=state.global_regime_confidence,
            risk_level=state.global_risk_level,
            risk_score=state.global_risk_score,
            strongest_currency={
                "symbol": strongest_curr.entity,
                "score": strongest_curr.score,
                "direction": strongest_curr.direction.value,
            }
            if strongest_curr
            else None,
            weakest_currency={
                "symbol": weakest_curr.entity,
                "score": weakest_curr.score,
                "direction": weakest_curr.direction.value,
            }
            if weakest_curr
            else None,
            strongest_asset_class={
                "name": strongest_asset.name,
                "score": strongest_asset.score,
                "direction": strongest_asset.direction.value,
            }
            if strongest_asset
            else None,
            weakest_asset_class={
                "name": weakest_asset.name,
                "score": weakest_asset.score,
                "direction": weakest_asset.direction.value,
            }
            if weakest_asset
            else None,
            top_currencies=top_currencies,
            top_asset_classes=top_asset_classes,
            top_drivers=state.global_drivers[:3],
            top_risks=[
                {"name": r.get("name", ""), "severity": r.get("severity", 0)}
                for r in state.global_risks[:3]
            ],
            executive_summary=state.executive_summary,
            generated_at=state.generated_at.isoformat(),
            valid_until=state.valid_until.isoformat(),
        )
