"""
Global Intelligence Hub - AI Executive Interpreter

Interprets the global configuration and provides narrative insights.
"""

import logging
from typing import Any

from ..state.state import GlobalHubState

logger = logging.getLogger(__name__)


class AIExecutiveInterpreter:
    """
    Interprets the global configuration.

    The AI receives structured facts and returns a narrative
    interpretation. It does NOT invent data - it only explains
    what the configuration suggests.

    This is a placeholder for actual LLM integration.
    For now, it returns template-based interpretations.
    """

    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm

    def interpret(
        self, state: GlobalHubState, structured_summary: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Generate AI interpretation from structured summary.

        Args:
            state: GlobalHubState
            structured_summary: Structured summary from DeterministicSummaryEngine

        Returns:
            Dict with AI interpretation
        """
        # Extract data
        regime = structured_summary.get("regime", "UNKNOWN")
        risk_level = structured_summary.get("risk_level", "UNKNOWN")
        strongest_currency = structured_summary.get("strongest_currency")
        risks = structured_summary.get("risks", [])

        # Build narrative
        narrative = self._build_narrative(
            regime=regime, risk_level=risk_level, strongest_currency=strongest_currency
        )

        # Build interpretation
        interpretation = self._build_interpretation(regime=regime)

        return {
            "narrative": narrative,
            "market_interpretation": interpretation,
            "capital_flow_interpretation": self._build_capital_flow_interpretation(
                strongest_currency=strongest_currency, regime=regime
            ),
            "dominant_theme": self._build_dominant_theme(regime=regime),
            "key_risk": risks[0] if risks else "No identified risks",
            "regime_outlook": self._build_regime_outlook(regime=regime),
            "what_could_change": self._build_change_triggers(regime=regime),
            "confidence": state.global_regime_confidence,
            "evidence_references": self._build_evidence_references(state),
        }

    def _build_narrative(self, **kwargs) -> str:
        """Build the narrative from structured facts."""
        parts = []

        regime = kwargs.get("regime", "UNKNOWN")
        risk_level = kwargs.get("risk_level", "UNKNOWN")
        strongest_currency = kwargs.get("strongest_currency")

        parts.append(f"The global environment is currently {regime}.")
        parts.append(f"The risk level is {risk_level}.")

        if strongest_currency:
            parts.append(f"{strongest_currency['entity']} is the strongest currency.")

        return " ".join(parts)

    def _build_interpretation(self, regime: str) -> str:
        """Build market interpretation."""
        if regime == "RISK_OFF":
            return "The market is defensive, with capital flowing toward safety."
        elif regime == "RISK_ON":
            return "The market is favoring growth-oriented assets, indicating risk appetite."
        else:
            return "The market is in transition with mixed signals."

    def _build_capital_flow_interpretation(self, **kwargs) -> str:
        """Build capital flow interpretation."""
        strongest_currency = kwargs.get("strongest_currency")
        regime = kwargs.get("regime", "UNKNOWN")

        if regime == "RISK_OFF":
            if strongest_currency and strongest_currency.get("entity") in [
                "USD",
                "JPY",
                "CHF",
            ]:
                return "Capital is flowing toward safe-haven currencies."
            return "Capital is flowing defensively."
        else:
            return "Capital is flowing toward growth opportunities."

    def _build_dominant_theme(self, regime: str) -> str:
        """Build dominant theme."""
        if regime == "RISK_OFF":
            return "Defensive capital rotation"
        elif regime == "RISK_ON":
            return "Risk-on positioning"
        else:
            return "Market transition"

    def _build_regime_outlook(self, regime: str) -> str:
        """Build regime outlook."""
        if regime == "RISK_OFF":
            return "Likely to persist unless risk appetite improves"
        elif regime == "RISK_ON":
            return "Likely to persist unless risk aversion increases"
        else:
            return "Uncertain, monitoring for directional signals"

    def _build_change_triggers(self, regime: str) -> str:
        """Build what could change the view."""
        triggers = []

        if regime == "RISK_OFF":
            triggers.append("A shift toward risk-on sentiment")
        elif regime == "RISK_ON":
            triggers.append("A shift toward risk-off sentiment")

        if not triggers:
            triggers.append("A significant regime change event")

        return f"Key change triggers: {' or '.join(triggers[:3])}."

    def _build_evidence_references(self, state: GlobalHubState) -> list[str]:
        """Build evidence references."""
        references = []

        if state.currency_rankings:
            references.append(
                f"Currency rankings: {len(state.currency_rankings)} currencies"
            )

        if state.asset_class_rankings:
            references.append(
                f"Asset-class rankings: {len(state.asset_class_rankings)} classes"
            )

        if state.global_drivers:
            references.append(f"Drivers: {', '.join(state.global_drivers[:3])}")

        return references[:3]
