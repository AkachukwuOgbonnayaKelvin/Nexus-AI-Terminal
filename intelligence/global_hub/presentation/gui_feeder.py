"""
Global Intelligence Hub - GUI Presentation Feeder

Prepares the final read-only presentation feed for the dashboard.
The dashboard is a mirror — it only displays what is computed here.
NO RECALCULATION happens in the GUI.
"""

import logging
from typing import Dict, Any
from datetime import datetime

from ..state.state import GlobalHubState
from ..summary.deterministic import DeterministicSummaryEngine
from ..ai.executive_interpreter import AIExecutiveInterpreter

logger = logging.getLogger(__name__)


class GUIPresentationFeeder:
    """
    Prepares the GUI presentation feed.

    This is the FINAL read-only output for the dashboard.
    The dashboard mirrors this data — it does not recalculate anything.
    """

    def __init__(self):
        self.summary_engine = DeterministicSummaryEngine()
        self.ai_interpreter = AIExecutiveInterpreter(use_llm=False)

    def prepare_feed(self, state: GlobalHubState) -> Dict[str, Any]:
        """
        Prepare the complete GUI presentation feed.

        Args:
            state: GlobalHubState

        Returns:
            Dict: Complete presentation feed
        """
        logger.info(f"Preparing GUI presentation feed for state {state.state_id}")

        # Generate summaries
        structured_summary = self.summary_engine.generate_structured_summary(state)
        ai_interpretation = self.ai_interpreter.interpret(state, structured_summary)

        return {
            "meta": self._prepare_meta(state),
            "overview": self._prepare_overview(state),
            "executive_summary": self._prepare_executive_summary(
                state, structured_summary
            ),
            "ai_executive_summary": self._prepare_ai_summary(ai_interpretation),
            "currency_intelligence": self._prepare_currency_intelligence(state),
            "asset_class_intelligence": self._prepare_asset_class_intelligence(state),
            "global_regime": self._prepare_regime(state),
            "global_risk": self._prepare_risk(state),
            "drivers": self._prepare_drivers(state),
            "themes": self._prepare_themes(state),
            "opportunities": self._prepare_opportunities(state),
            "risks": self._prepare_risks(state),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _prepare_meta(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare metadata with lineage."""
        return {
            "state_id": state.state_id,
            "generated_at": state.generated_at.isoformat(),
            "valid_until": state.valid_until.isoformat(),
            "schema_version": state.schema_version,
            "producer": "GLOBAL_INTELLIGENCE_HUB",
            "is_valid": state.is_valid,
            "age_seconds": state.age_seconds(),
            "freshness_status": self._get_freshness_status(state),
            "previous_state_id": state.previous_state_id,
        }

    def _get_freshness_status(self, state: GlobalHubState) -> str:
        """Get freshness status."""
        if state.is_expired():
            return "EXPIRED"
        age = state.age_seconds()
        if age < 600:
            return "CURRENT"
        elif age < 1800:
            return "AGING"
        elif age < 3600:
            return "STALE"
        else:
            return "EXPIRED"

    def _prepare_overview(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare overview data."""
        strongest_curr = state.get_strongest_currency()
        weakest_curr = state.get_weakest_currency()
        strongest_asset = state.get_strongest_asset_class()
        weakest_asset = state.get_weakest_asset_class()

        return {
            "regime": state.global_regime,
            "regime_confidence": state.global_regime_confidence,
            "risk_level": state.global_risk_level,
            "risk_score": state.global_risk_score,
            "strongest_currency": {
                "symbol": strongest_curr.entity if strongest_curr else None,
                "score": strongest_curr.score if strongest_curr else None,
                "direction": strongest_curr.direction.value if strongest_curr else None,
                "confidence": strongest_curr.confidence if strongest_curr else None,
            }
            if strongest_curr
            else None,
            "weakest_currency": {
                "symbol": weakest_curr.entity if weakest_curr else None,
                "score": weakest_curr.score if weakest_curr else None,
                "direction": weakest_curr.direction.value if weakest_curr else None,
                "confidence": weakest_curr.confidence if weakest_curr else None,
            }
            if weakest_curr
            else None,
            "strongest_asset_class": {
                "name": strongest_asset.name if strongest_asset else None,
                "score": strongest_asset.score if strongest_asset else None,
                "direction": strongest_asset.direction.value
                if strongest_asset
                else None,
                "confidence": strongest_asset.confidence if strongest_asset else None,
            }
            if strongest_asset
            else None,
            "weakest_asset_class": {
                "name": weakest_asset.name if weakest_asset else None,
                "score": weakest_asset.score if weakest_asset else None,
                "direction": weakest_asset.direction.value if weakest_asset else None,
                "confidence": weakest_asset.confidence if weakest_asset else None,
            }
            if weakest_asset
            else None,
        }

    def _prepare_executive_summary(
        self, state: GlobalHubState, structured: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare executive summary."""
        return {
            "text": structured.get("summary_text", state.executive_summary),
            "regime": state.global_regime,
            "risk_level": state.global_risk_level,
            "confidence": state.global_regime_confidence,
            "strongest_currency": structured.get("strongest_currency"),
            "weakest_currency": structured.get("weakest_currency"),
            "strongest_asset": structured.get("strongest_asset_class"),
            "weakest_asset": structured.get("weakest_asset_class"),
            "drivers": structured.get("drivers", []),
            "risks": structured.get("risks", []),
            "themes": structured.get("themes", []),
        }

    def _prepare_ai_summary(self, interpretation: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare AI executive summary."""
        return {
            "narrative": interpretation.get("narrative", ""),
            "market_interpretation": interpretation.get("market_interpretation", ""),
            "capital_flow_interpretation": interpretation.get(
                "capital_flow_interpretation", ""
            ),
            "dominant_theme": interpretation.get("dominant_theme", ""),
            "key_risk": interpretation.get("key_risk", ""),
            "regime_outlook": interpretation.get("regime_outlook", ""),
            "what_could_change": interpretation.get("what_could_change", ""),
            "confidence": interpretation.get("confidence", 0.0),
            "evidence_references": interpretation.get("evidence_references", []),
        }

    def _prepare_currency_intelligence(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare currency intelligence with lineage."""
        return {
            "rankings": [
                {
                    "rank": c.rank,
                    "symbol": c.entity,
                    "score": c.score,
                    "direction": c.direction.value,
                    "confidence": c.confidence,
                    "evidence_count": c.evidence_count
                    if hasattr(c, "evidence_count")
                    else None,
                    "supporting_engines": c.supporting_engines[:5]
                    if hasattr(c, "supporting_engines")
                    else [],
                    "drivers": [d.name for d in c.drivers[:3]]
                    if hasattr(c, "drivers")
                    else [],
                }
                for c in state.currency_rankings
            ],
            "count": len(state.currency_rankings),
            "strongest": state.get_strongest_currency().entity
            if state.get_strongest_currency()
            else None,
            "weakest": state.get_weakest_currency().entity
            if state.get_weakest_currency()
            else None,
        }

    def _prepare_asset_class_intelligence(
        self, state: GlobalHubState
    ) -> Dict[str, Any]:
        """Prepare asset-class intelligence."""
        return {
            "rankings": [
                {
                    "rank": a.rank,
                    "name": a.name,
                    "asset_class": a.asset_class.value,
                    "score": a.score,
                    "direction": a.direction.value,
                    "confidence": a.confidence,
                }
                for a in state.asset_class_rankings
            ],
            "count": len(state.asset_class_rankings),
            "strongest": state.get_strongest_asset_class().name
            if state.get_strongest_asset_class()
            else None,
            "weakest": state.get_weakest_asset_class().name
            if state.get_weakest_asset_class()
            else None,
        }

    def _prepare_regime(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare regime data."""
        return {
            "regime": state.global_regime,
            "confidence": state.global_regime_confidence,
            "risk_level": state.global_risk_level,
            "risk_score": state.global_risk_score,
            "interpretation": self._get_regime_interpretation(state.global_regime),
        }

    def _get_regime_interpretation(self, regime: str) -> str:
        """Get human-readable regime interpretation."""
        interpretations = {
            "RISK_ON": "Risk appetite is elevated. Capital flowing toward growth assets.",
            "RISK_OFF": "Risk aversion is elevated. Capital flowing toward safe-haven assets.",
            "TRENDING": "Markets are exhibiting strong directional momentum.",
            "RANGING": "Markets are consolidating within a range.",
            "TRANSITION": "Markets are transitioning between regimes.",
            "UNKNOWN": "Regime classification is uncertain.",
        }
        return interpretations.get(regime, "Regime classification unknown.")

    def _prepare_risk(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare risk data."""
        return {
            "level": state.global_risk_level,
            "score": state.global_risk_score,
            "confidence": state.global_regime_confidence,
            "risks": [
                {
                    "name": r.get("name", "Unknown risk"),
                    "severity": r.get("severity", 0),
                    "description": r.get("description", ""),
                }
                for r in state.global_risks[:5]
            ],
        }

    def _prepare_drivers(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare drivers data."""
        return {"drivers": state.global_drivers, "count": len(state.global_drivers)}

    def _prepare_themes(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare themes data."""
        return {
            "themes": [
                {
                    "name": t.get("name", "Unknown theme"),
                    "strength": t.get("strength", 0),
                    "description": t.get("description", ""),
                }
                for t in state.global_themes[:5]
            ],
            "count": len(state.global_themes),
        }

    def _prepare_opportunities(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare opportunities data."""
        return {
            "opportunities": state.top_opportunities[:5],
            "count": len(state.top_opportunities),
        }

    def _prepare_risks(self, state: GlobalHubState) -> Dict[str, Any]:
        """Prepare risks data."""
        return {
            "risks": [
                {
                    "name": r.get("name", "Unknown risk"),
                    "severity": r.get("severity", 0),
                    "affected_assets": r.get("affected_assets", []),
                }
                for r in state.global_risks[:5]
            ],
            "count": len(state.global_risks),
        }
