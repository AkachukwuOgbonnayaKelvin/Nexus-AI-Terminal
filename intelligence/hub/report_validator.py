"""
Global Intelligence Hub - Report Validator
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ReportValidator:
    """
    Validates intelligence reports before they enter the hub.
    """

    def validate(self, report: Any) -> dict[str, Any]:
        """
        Validate a single report.

        Args:
            report: Engine report

        Returns:
            Validation result
        """
        if report is None:
            return {"valid": False, "reason": "Report is None"}

        # Check required attributes
        required_attrs = ["engine_id", "engine_name", "confidence"]
        missing = [attr for attr in required_attrs if not hasattr(report, attr)]

        if missing:
            return {"valid": False, "reason": f"Missing attributes: {missing}"}

        return {"valid": True, "reason": "OK"}

    def validate_all(self, reports: dict[str, Any]) -> dict[str, Any]:
        """
        Validate all reports.

        Args:
            reports: Dictionary of engine_id → report

        Returns:
            Validation results for all reports
        """
        results = {}
        all_valid = True

        for engine_id, report in reports.items():
            result = self.validate(report)
            results[engine_id] = result
            if not result["valid"]:
                all_valid = False

        return {"all_valid": all_valid, "results": results}
