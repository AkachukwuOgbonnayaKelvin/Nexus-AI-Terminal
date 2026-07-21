"""
Global Intelligence Hub - Confidence Engine
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfidenceEngine:
    """
    Calculates overall confidence from multiple intelligence reports.

    The confidence engine aggregates confidence scores from all available
    intelligence engines and produces a unified confidence metric for
    the Global Intelligence Snapshot.
    """

    def __init__(self):
        self.last_calculation: Optional[Dict[str, Any]] = None

    def calculate_confidence(self, reports: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall confidence across all reports.

        Args:
            reports: Dictionary of engine_id → report

        Returns:
            Confidence dictionary with overall confidence and components
        """
        if not reports:
            return {
                "overall_confidence": 0.0,
                "status": "NO_REPORTS",
                "components": {},
                "component_count": 0,
            }

        components = {}
        weighted_sum = 0.0
        total_weight = 0.0

        # Engine weights based on importance
        weights = {
            "GLB-001": 0.40,  # Market regime is primary
            "GLB-002": 0.30,  # Asset impact
            "GLB-003": 0.30,  # Macro conditions
        }

        for engine_id, report in reports.items():
            if report is None:
                continue

            weight = weights.get(engine_id, 0.20)
            confidence = self._extract_confidence(report)

            if confidence is not None:
                components[engine_id] = {
                    "confidence": confidence,
                    "weight": weight,
                    "contribution": confidence * weight,
                    "report_available": True,
                }
                weighted_sum += confidence * weight
                total_weight += weight

        if total_weight == 0:
            return {
                "overall_confidence": 0.0,
                "status": "NO_CONFIDENCE_DATA",
                "components": components,
                "component_count": len(components),
            }

        overall = weighted_sum / total_weight
        overall = min(100.0, max(0.0, overall))

        # Determine status based on number of components
        if len(components) >= 3:
            status = "HIGH"
        elif len(components) >= 2:
            status = "MEDIUM"
        elif len(components) >= 1:
            status = "LOW"
        else:
            status = "NONE"

        self.last_calculation = {
            "overall_confidence": overall,
            "status": status,
            "components": components,
            "component_count": len(components),
            "weighted_sum": weighted_sum,
            "total_weight": total_weight,
        }

        return self.last_calculation

    def _extract_confidence(self, report: Any) -> Optional[float]:
        """Extract confidence from a report."""
        if report is None:
            return None

        # Try different ways to get confidence
        if hasattr(report, "confidence"):
            try:
                return float(report.confidence)
            except (ValueError, TypeError):
                pass

        if hasattr(report, "overall_confidence"):
            try:
                return float(report.overall_confidence)
            except (ValueError, TypeError):
                pass

        if hasattr(report, "confidence_score"):
            try:
                return float(report.confidence_score)
            except (ValueError, TypeError):
                pass

        if hasattr(report, "get_confidence"):
            try:
                return float(report.get_confidence())
            except (ValueError, TypeError):
                pass

        if isinstance(report, dict):
            for key in ["confidence", "overall_confidence", "confidence_score"]:
                if key in report:
                    try:
                        return float(report[key])
                    except (ValueError, TypeError):
                        pass

        return None

    def get_last_calculation(self) -> Optional[Dict[str, Any]]:
        """Get the last confidence calculation."""
        return self.last_calculation

    def health_check(self) -> Dict[str, Any]:
        """Check confidence engine health."""
        return {
            "status": "OPERATIONAL",
            "last_calculation": self.last_calculation is not None,
        }
