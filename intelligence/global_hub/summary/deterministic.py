"""
Global Intelligence Hub - Deterministic Summary Engine

Produces fact-based, auditable executive summaries.
"""

import logging
from typing import Dict, Any

from ..state.state import GlobalHubState

logger = logging.getLogger(__name__)


class DeterministicSummaryEngine:
    """
    Produces deterministic executive summaries from canonical state.

    This is NOT generative AI. It is a structured, auditable,
    reproducible summary builder.
    """

    def __init__(self):
        self._templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load summary templates."""
        return {
            "regime": "The current global environment is {regime}.",
            "risk": "The global risk level is {risk_level} with a score of {risk_score:.1f}.",
            "strongest_currency": "{entity} is the strongest currency at {score:+.1f}.",
            "weakest_currency": "{entity} is the weakest currency at {score:+.1f}.",
            "strongest_asset": "{name} is the strongest asset class at {score:+.1f}.",
            "weakest_asset": "{name} is the weakest asset class at {score:+.1f}.",
            "drivers": "Key drivers include: {drivers}.",
            "risks": "Key risks include: {risks}.",
            "themes": "Dominant themes include: {themes}.",
            "confidence": "Confidence in this assessment is {confidence:.1f}%.",
        }

    def generate_summary(self, state: GlobalHubState) -> str:
        """
        Generate a deterministic executive summary.

        Args:
            state: GlobalHubState

        Returns:
            str: Executive summary
        """
        parts = []

        # Regime
        parts.append(self._templates["regime"].format(regime=state.global_regime))

        # Risk
        parts.append(
            self._templates["risk"].format(
                risk_level=state.global_risk_level, risk_score=state.global_risk_score
            )
        )

        # Strongest currency
        strongest = state.get_strongest_currency()
        if strongest:
            parts.append(
                self._templates["strongest_currency"].format(
                    entity=strongest.entity, score=strongest.score
                )
            )

        # Weakest currency
        weakest = state.get_weakest_currency()
        if weakest and weakest.score < 0:
            parts.append(
                self._templates["weakest_currency"].format(
                    entity=weakest.entity, score=weakest.score
                )
            )

        # Strongest asset
        strongest_asset = state.get_strongest_asset_class()
        if strongest_asset:
            parts.append(
                self._templates["strongest_asset"].format(
                    name=strongest_asset.name, score=strongest_asset.score
                )
            )

        # Weakest asset
        weakest_asset = state.get_weakest_asset_class()
        if weakest_asset and weakest_asset.score < 0:
            parts.append(
                self._templates["weakest_asset"].format(
                    name=weakest_asset.name, score=weakest_asset.score
                )
            )

        # Drivers
        if state.global_drivers:
            parts.append(
                self._templates["drivers"].format(
                    drivers=", ".join(state.global_drivers[:3])
                )
            )

        # Risks
        if state.global_risks:
            risk_names = [r.get("name", "") for r in state.global_risks[:3]]
            if risk_names:
                parts.append(
                    self._templates["risks"].format(risks=", ".join(risk_names))
                )

        # Themes
        if state.global_themes:
            theme_names = [t.get("name", "") for t in state.global_themes[:3]]
            if theme_names:
                parts.append(
                    self._templates["themes"].format(themes=", ".join(theme_names))
                )

        # Confidence
        parts.append(
            self._templates["confidence"].format(
                confidence=state.global_regime_confidence
            )
        )

        summary = " ".join(parts)
        logger.info(f"Generated deterministic summary ({len(summary)} chars)")
        return summary

    def generate_structured_summary(self, state: GlobalHubState) -> Dict[str, Any]:
        """
        Generate a structured executive summary.

        Returns:
            Dict with structured summary fields
        """
        return {
            "regime": state.global_regime,
            "risk_level": state.global_risk_level,
            "risk_score": state.global_risk_score,
            "strongest_currency": {
                "entity": state.get_strongest_currency().entity
                if state.get_strongest_currency()
                else None,
                "score": state.get_strongest_currency().score
                if state.get_strongest_currency()
                else None,
            }
            if state.get_strongest_currency()
            else None,
            "weakest_currency": {
                "entity": state.get_weakest_currency().entity
                if state.get_weakest_currency()
                else None,
                "score": state.get_weakest_currency().score
                if state.get_weakest_currency()
                else None,
            }
            if state.get_weakest_currency()
            else None,
            "strongest_asset_class": {
                "name": state.get_strongest_asset_class().name
                if state.get_strongest_asset_class()
                else None,
                "score": state.get_strongest_asset_class().score
                if state.get_strongest_asset_class()
                else None,
            }
            if state.get_strongest_asset_class()
            else None,
            "weakest_asset_class": {
                "name": state.get_weakest_asset_class().name
                if state.get_weakest_asset_class()
                else None,
                "score": state.get_weakest_asset_class().score
                if state.get_weakest_asset_class()
                else None,
            }
            if state.get_weakest_asset_class()
            else None,
            "drivers": state.global_drivers[:3],
            "risks": [r.get("name", "") for r in state.global_risks[:3]],
            "themes": [t.get("name", "") for t in state.global_themes[:3]],
            "confidence": state.global_regime_confidence,
            "summary_text": self.generate_summary(state),
        }
