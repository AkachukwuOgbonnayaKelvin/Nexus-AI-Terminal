"""
Global Intelligence Hub - Consensus Engine
"""

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ConsensusEngine:
    """
    Calculates consensus from multiple intelligence reports.
    """

    def calculate_consensus(self, reports: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate consensus across all reports.

        Args:
            reports: Dictionary of engine_id → report

        Returns:
            Consensus dictionary
        """
        if not reports:
            return {"status": "NO_REPORTS", "consensus_score": 0, "confidence": 0}

        # Extract regime if available
        regime_consensus = self._calculate_regime_consensus(reports)

        # Extract asset consensus if available
        asset_consensus = self._calculate_asset_consensus(reports)

        # Calculate overall consensus score
        overall_score = self._calculate_overall_score(reports)

        return {
            "status": "OPERATIONAL" if len(reports) >= 2 else "PARTIAL",
            "regime": regime_consensus,
            "assets": asset_consensus,
            "overall_score": overall_score,
            "engine_count": len(reports),
            "generated_at": datetime.utcnow().isoformat(),
        }

    def _calculate_regime_consensus(self, reports: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate consensus on market regime."""
        regimes = []

        # Try to get regime from GLB-001
        if "GLB-001" in reports and reports["GLB-001"]:
            report = reports["GLB-001"]
            if hasattr(report, "primary_regime"):
                regimes.append(
                    {
                        "source": "GLB-001",
                        "regime": report.primary_regime.value,
                        "score": report.regime_score,
                        "confidence": report.confidence,
                    }
                )

        if not regimes:
            return {"status": "NO_REGIME_DATA", "primary_regime": "UNKNOWN"}

        # Find the regime with the highest confidence
        best = max(regimes, key=lambda x: x.get("confidence", 0))

        return {
            "status": "CONSENSUS",
            "primary_regime": best["regime"],
            "confidence": best["confidence"],
            "sources": regimes,
            "agreement": len(regimes) > 1,
        }

    def _calculate_asset_consensus(self, reports: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate consensus on asset biases."""
        asset_biases = {}

        # Try to get asset data from GLB-002
        if "GLB-002" in reports and reports["GLB-002"]:
            report = reports["GLB-002"]
            if hasattr(report, "asset_reports"):
                for asset, data in report.asset_reports.items():
                    if asset not in asset_biases:
                        asset_biases[asset] = []
                    asset_biases[asset].append(
                        {
                            "source": "GLB-002",
                            "bias": data.get("bias"),
                            "score": data.get("score"),
                            "confidence": data.get("confidence"),
                        }
                    )

        return asset_biases

    def _calculate_overall_score(self, reports: Dict[str, Any]) -> float:
        """Calculate overall consensus score."""
        scores = []
        weights = {
            "GLB-001": 0.4,  # Market regime is primary
            "GLB-002": 0.3,  # Asset impact
            "GLB-003": 0.3,  # Macro conditions
        }

        for engine_id, report in reports.items():
            if not report:
                continue
            weight = weights.get(engine_id, 0.2)
            if hasattr(report, "regime_score"):
                scores.append(report.regime_score * weight)
            elif hasattr(report, "overall_score"):
                scores.append(report.overall_score * weight)

        if not scores:
            return 0

        return sum(scores) / len(scores)
