"""
Confluence Engine - Input Gate

Validates, timestamps, and checks incoming GLB reports.
"""

import logging
from typing import Dict, Any
from datetime import datetime

from .registry import EngineRegistry

logger = logging.getLogger(__name__)


class InputGate:
    """
    Validates incoming GLB reports before they enter the Confluence Engine.
    """

    def __init__(self, max_age_seconds: int = 3600):
        self.max_age_seconds = max_age_seconds
        self.registry = EngineRegistry()

    def validate_report(self, engine_id: str, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single engine report.

        Returns:
            Dict with validation result and any issues
        """
        result = {
            "engine_id": engine_id,
            "valid": True,
            "issues": [],
            "warnings": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Check if engine is known
        engine_entry = self.registry.get(engine_id)
        if not engine_entry:
            result["valid"] = False
            result["issues"].append(f"Unknown engine: {engine_id}")
            return result

        # Check if report has required fields
        required_fields = ["engine_id", "engine_name", "status"]
        for field in required_fields:
            if field not in report:
                result["valid"] = False
                result["issues"].append(f"Missing required field: {field}")

        # Check status
        if report.get("status") != "OPERATIONAL":
            result["warnings"].append(f"Engine status: {report.get('status')}")

        # Check for core intelligence
        if "core_intelligence" not in report and "asset_impact_matrix" not in report:
            result["warnings"].append(
                "No core_intelligence or asset_impact_matrix found"
            )

        # Check for generated_at timestamp
        if "generated_at" in report:
            try:
                gen_time = datetime.fromisoformat(
                    report["generated_at"].replace("Z", "+00:00")
                )
                age = (datetime.utcnow() - gen_time).total_seconds()
                if age > self.max_age_seconds:
                    result["warnings"].append(
                        f"Report is {age:.0f}s old (max: {self.max_age_seconds}s)"
                    )
            except Exception:
                pass

        return result

    def validate_reports(self, reports: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate multiple engine reports.

        Returns:
            Dict with validation results for all engines
        """
        results = {}
        valid_reports = {}
        missing_engines = []

        # Check which engines have reports
        all_engines = self.registry.get_engine_ids()
        for engine_id in all_engines:
            if engine_id in reports and reports[engine_id] is not None:
                validation = self.validate_report(engine_id, reports[engine_id])
                results[engine_id] = validation
                if validation["valid"]:
                    valid_reports[engine_id] = reports[engine_id]
            else:
                missing_engines.append(engine_id)
                results[engine_id] = {
                    "engine_id": engine_id,
                    "valid": False,
                    "issues": ["Report missing"],
                    "warnings": [],
                    "timestamp": datetime.utcnow().isoformat(),
                }

        return {
            "results": results,
            "valid_reports": valid_reports,
            "missing_engines": missing_engines,
            "total_engines": len(all_engines),
            "valid_count": len(valid_reports),
            "missing_count": len(missing_engines),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_freshness(self, report: Dict[str, Any]) -> float:
        """
        Get freshness score (0-1) for a report.
        """
        if "generated_at" not in report:
            return 0.5

        try:
            gen_time = datetime.fromisoformat(
                report["generated_at"].replace("Z", "+00:00")
            )
            age = (datetime.utcnow() - gen_time).total_seconds()

            # Freshness decays from 1.0 to 0.0 over max_age_seconds
            freshness = max(0.0, 1.0 - (age / self.max_age_seconds))
            return freshness
        except Exception:
            return 0.5
