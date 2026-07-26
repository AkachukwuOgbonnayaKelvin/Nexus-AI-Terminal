"""
Global Intelligence Hub - Orchestrator Feeder

Prepares the decision context feed for the Master Orchestrator.
This is a compact, decision-ready output — NOT a presentation feed.
"""

import logging
from datetime import datetime
from typing import Any

from ..state.state import GlobalHubState

logger = logging.getLogger(__name__)


class OrchestratorFeeder:
    """
    Prepares the Orchestrator decision feed.

    This is a compact decision-context output for the Master Orchestrator.
    It contains only what the Orchestrator needs to make cross-domain decisions.
    """

    def prepare_feed(self, state: GlobalHubState) -> dict[str, Any]:
        """
        Prepare the Orchestrator decision feed.

        Args:
            state: GlobalHubState

        Returns:
            Dict: Decision context feed
        """
        logger.info(f"Preparing Orchestrator feed for state {state.state_id}")

        return {
            "meta": self._prepare_meta(state),
            "global_context": self._prepare_global_context(state),
            "currency_context": self._prepare_currency_context(state),
            "asset_class_context": self._prepare_asset_class_context(state),
            "decision_context": self._prepare_decision_context(state),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _prepare_meta(self, state: GlobalHubState) -> dict[str, Any]:
        """Prepare metadata."""
        return {
            "state_id": state.state_id,
            "generated_at": state.generated_at.isoformat(),
            "valid_until": state.valid_until.isoformat(),
            "schema_version": state.schema_version,
            "is_valid": state.is_valid,
            "source": "GLOBAL_INTELLIGENCE_HUB",
            "confidence": state.global_regime_confidence,
        }

    def _prepare_global_context(self, state: GlobalHubState) -> dict[str, Any]:
        """Prepare global context."""
        return {
            "regime": state.global_regime,
            "regime_confidence": state.global_regime_confidence,
            "risk_level": state.global_risk_level,
            "risk_score": state.global_risk_score,
            "dominant_theme": self._get_dominant_theme(state),
        }

    def _get_dominant_theme(self, state: GlobalHubState) -> str:
        """Get the dominant theme."""
        if state.global_themes:
            sorted_themes = sorted(
                state.global_themes, key=lambda t: t.get("strength", 0), reverse=True
            )
            if sorted_themes:
                return sorted_themes[0].get("name", "Unknown theme")
        return "No dominant theme identified"

    def _prepare_currency_context(self, state: GlobalHubState) -> dict[str, Any]:
        """Prepare currency context."""
        currencies = []
        for c in state.currency_rankings:
            currencies.append(
                {
                    "symbol": c.entity,
                    "score": c.score,
                    "direction": c.direction.value,
                    "confidence": c.confidence,
                    "rank": c.rank,
                }
            )

        return {
            "currencies": currencies,
            "count": len(currencies),
            "strongest": state.get_strongest_currency().entity
            if state.get_strongest_currency()
            else None,
            "weakest": state.get_weakest_currency().entity
            if state.get_weakest_currency()
            else None,
        }

    def _prepare_asset_class_context(self, state: GlobalHubState) -> dict[str, Any]:
        """Prepare asset-class context."""
        asset_classes = []
        for a in state.asset_class_rankings:
            asset_classes.append(
                {
                    "name": a.name,
                    "asset_class": a.asset_class.value,
                    "score": a.score,
                    "direction": a.direction.value,
                    "confidence": a.confidence,
                    "rank": a.rank,
                }
            )

        return {
            "asset_classes": asset_classes,
            "count": len(asset_classes),
            "strongest": state.get_strongest_asset_class().name
            if state.get_strongest_asset_class()
            else None,
            "weakest": state.get_weakest_asset_class().name
            if state.get_weakest_asset_class()
            else None,
        }

    def _prepare_decision_context(self, state: GlobalHubState) -> dict[str, Any]:
        """
        Prepare the compact decision context.

        This is what the Master Orchestrator actually needs.
        """
        return {
            "regime_signal": self._get_regime_signal(state),
            "risk_signal": self._get_risk_signal(state),
            "currency_bias": self._get_currency_bias(state),
            "asset_class_bias": self._get_asset_class_bias(state),
            "key_drivers": state.global_drivers[:5],
            "key_risks": [r.get("name", "") for r in state.global_risks[:3]],
            "opportunities": [
                {
                    "entity": o.get("entity", ""),
                    "score": o.get("score", 0),
                    "direction": o.get("direction", ""),
                    "confidence": o.get("confidence", 0),
                }
                for o in state.top_opportunities[:3]
            ],
            "consensus_confidence": state.global_regime_confidence,
        }

    def _get_regime_signal(self, state: GlobalHubState) -> dict[str, Any]:
        """Get regime signal for orchestrator."""
        return {
            "regime": state.global_regime,
            "confidence": state.global_regime_confidence,
            "strength": self._get_regime_strength(
                state.global_regime, state.global_regime_confidence
            ),
        }

    def _get_regime_strength(self, regime: str, confidence: float) -> str:
        """Get regime strength descriptor."""
        if confidence >= 80:
            return "STRONG"
        elif confidence >= 60:
            return "MODERATE"
        elif confidence >= 40:
            return "WEAK"
        else:
            return "UNCERTAIN"

    def _get_risk_signal(self, state: GlobalHubState) -> dict[str, Any]:
        """Get risk signal for orchestrator."""
        return {"level": state.global_risk_level, "score": state.global_risk_score}

    def _get_currency_bias(self, state: GlobalHubState) -> dict[str, Any]:
        """Get currency bias summary."""
        bullish = [
            c.entity for c in state.currency_rankings if c.direction.value == "BULLISH"
        ]
        bearish = [
            c.entity for c in state.currency_rankings if c.direction.value == "BEARISH"
        ]
        neutral = [
            c.entity for c in state.currency_rankings if c.direction.value == "NEUTRAL"
        ]

        return {
            "bullish": bullish[:3],
            "bearish": bearish[:3],
            "neutral": neutral[:3],
            "bullish_count": len(bullish),
            "bearish_count": len(bearish),
            "neutral_count": len(neutral),
        }

    def _get_asset_class_bias(self, state: GlobalHubState) -> dict[str, Any]:
        """Get asset-class bias summary."""
        bullish = [
            a.name for a in state.asset_class_rankings if a.direction.value == "BULLISH"
        ]
        bearish = [
            a.name for a in state.asset_class_rankings if a.direction.value == "BEARISH"
        ]
        neutral = [
            a.name for a in state.asset_class_rankings if a.direction.value == "NEUTRAL"
        ]

        return {
            "bullish": bullish[:3],
            "bearish": bearish[:3],
            "neutral": neutral[:3],
            "bullish_count": len(bullish),
            "bearish_count": len(bearish),
            "neutral_count": len(neutral),
        }
