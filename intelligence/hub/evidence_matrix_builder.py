"""
Global Intelligence Hub - Evidence Matrix Builder
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class EvidenceMatrixBuilder:
    """Builds evidence matrix from all reports."""

    def build_matrix(self, reports: Dict[str, Any]) -> Dict[str, Any]:
        """Build evidence matrix."""
        evidence = []

        for engine_id, report in reports.items():
            if not report:
                continue

            if hasattr(report, "evidence") and report.evidence:
                for ev in report.evidence:
                    evidence.append(
                        {
                            "engine": engine_id,
                            "source": ev.source if hasattr(ev, "source") else "UNKNOWN",
                            "indicator": ev.indicator
                            if hasattr(ev, "indicator")
                            else "UNKNOWN",
                            "value": ev.value if hasattr(ev, "value") else None,
                            "direction": ev.direction
                            if hasattr(ev, "direction")
                            else "NEUTRAL",
                            "contribution": ev.contribution
                            if hasattr(ev, "contribution")
                            else 0,
                        }
                    )

        return {
            "total_evidence": len(evidence),
            "evidence": evidence,
            "status": "OPERATIONAL" if evidence else "NO_EVIDENCE",
        }
