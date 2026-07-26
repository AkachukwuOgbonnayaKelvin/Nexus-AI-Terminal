"""
Global Intelligence Hub - Conflict Resolver
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ConflictResolver:
    """
    Resolves conflicts between conflicting intelligence reports.
    """

    def resolve(self, reports: dict[str, Any]) -> dict[str, Any]:
        """
        Resolve conflicts between reports.

        Args:
            reports: Dictionary of engine_id → report

        Returns:
            Resolved consensus
        """
        if not reports:
            return {"status": "NO_REPORTS"}

        # Find the report with highest confidence
        best_engine = None
        best_confidence = -1

        for engine_id, report in reports.items():
            if report is None:
                continue

            confidence = getattr(report, "confidence", 0)
            if confidence > best_confidence:
                best_confidence = confidence
                best_engine = engine_id

        return {
            "status": "RESOLVED",
            "primary_engine": best_engine,
            "confidence": best_confidence,
        }
