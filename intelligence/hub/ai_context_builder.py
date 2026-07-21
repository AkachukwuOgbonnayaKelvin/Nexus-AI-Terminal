"""
Global Intelligence Hub - AI Context Builder
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AIContextBuilder:
    """Builds AI context for the workspace."""

    def build(
        self,
        regime_report: Any,
        asset_report: Any,
        macro_report: Any,
        consensus: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build AI context."""
        return {
            "regime_context": self._build_regime_context(regime_report),
            "asset_context": self._build_asset_context(asset_report),
            "macro_context": self._build_macro_context(macro_report),
            "consensus_context": consensus.get("regime_consensus", {}).get(
                "primary_regime", "UNKNOWN"
            ),
            "available": bool(regime_report or asset_report or macro_report),
        }

    def _build_regime_context(self, report: Any) -> Dict[str, Any]:
        if not report:
            return {"available": False}
        return {
            "available": True,
            "regime": report.primary_regime.value
            if hasattr(report, "primary_regime")
            else "UNKNOWN",
            "score": report.regime_score if hasattr(report, "regime_score") else 0,
            "confidence": report.confidence if hasattr(report, "confidence") else 0,
        }

    def _build_asset_context(self, report: Any) -> Dict[str, Any]:
        if not report:
            return {"available": False}
        return {
            "available": True,
            "asset_count": len(report.asset_reports)
            if hasattr(report, "asset_reports")
            else 0,
        }

    def _build_macro_context(self, report: Any) -> Dict[str, Any]:
        if not report:
            return {"available": False}
        return {
            "available": True,
            "score": report.overall_score if hasattr(report, "overall_score") else 0,
        }
