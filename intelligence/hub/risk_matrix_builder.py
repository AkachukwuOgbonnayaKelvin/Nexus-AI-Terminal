"""
Global Intelligence Hub - Risk Matrix Builder
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class RiskMatrixBuilder:
    """Builds risk matrix from all reports."""

    def build_matrix(self, reports: Dict[str, Any]) -> Dict[str, Any]:
        """Build risk matrix."""
        risks = []

        for engine_id, report in reports.items():
            if not report:
                continue

            if hasattr(report, "risks") and report.risks:
                for risk in report.risks:
                    risks.append(
                        {
                            "engine": engine_id,
                            "description": risk.description
                            if hasattr(risk, "description")
                            else "Unknown risk",
                            "probability": risk.probability
                            if hasattr(risk, "probability")
                            else 0,
                            "impact": risk.impact
                            if hasattr(risk, "impact")
                            else "MEDIUM",
                            "time_horizon": risk.time_horizon
                            if hasattr(risk, "time_horizon")
                            else "MEDIUM_TERM",
                        }
                    )

        return {
            "total_risks": len(risks),
            "risks": risks,
            "status": "OPERATIONAL" if risks else "NO_RISKS",
        }
