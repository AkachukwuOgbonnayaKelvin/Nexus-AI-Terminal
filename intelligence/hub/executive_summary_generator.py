"""
Global Intelligence Hub - Executive Summary Generator
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ExecutiveSummaryGenerator:
    """Generates executive summary from all reports."""

    def generate(
        self,
        regime_report: Any,
        asset_report: Any,
        macro_report: Any,
        consensus: Dict[str, Any],
    ) -> str:
        """Generate executive summary."""
        summary_parts = []

        # Regime summary
        if regime_report:
            regime = (
                regime_report.primary_regime.value
                if hasattr(regime_report, "primary_regime")
                else "UNKNOWN"
            )
            score = (
                regime_report.regime_score
                if hasattr(regime_report, "regime_score")
                else 0
            )
            confidence = (
                regime_report.confidence if hasattr(regime_report, "confidence") else 0
            )
            summary_parts.append(
                f"Market Regime: {regime} (Score: {score:.1f}, Confidence: {confidence:.1f}%)"
            )

        # Macro summary
        if macro_report:
            score = (
                macro_report.overall_score
                if hasattr(macro_report, "overall_score")
                else 0
            )
            summary_parts.append(f"Macro Conditions: Score {score:.1f}")

        # Asset summary
        if asset_report:
            asset_count = (
                len(asset_report.asset_reports)
                if hasattr(asset_report, "asset_reports")
                else 0
            )
            summary_parts.append(f"Assets Analyzed: {asset_count}")

        # Consensus
        if consensus:
            regime = consensus.get("regime_consensus", {}).get(
                "primary_regime", "UNKNOWN"
            )
            summary_parts.append(f"Consensus Regime: {regime}")

        if not summary_parts:
            return "No intelligence data available."

        return "\n".join(summary_parts)
