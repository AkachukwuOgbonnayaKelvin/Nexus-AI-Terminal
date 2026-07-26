"""
Global Intelligence Hub - Report Collector
"""

import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class ReportCollector:
    """
    Collects reports from all Global Intelligence engines.
    """

    def __init__(self):
        self.reports: dict[str, dict[str, Any]] = {
            "GLB-001": {"report": None, "collected_at": None},
            "GLB-002": {"report": None, "collected_at": None},
            "GLB-003": {"report": None, "collected_at": None},
        }
        self.all_collected = False

    def collect_report(self, engine_id: str, report: Any) -> bool:
        """
        Collect a report from an engine.

        Args:
            engine_id: "GLB-001", "GLB-002", or "GLB-003"
            report: The engine report (must be a valid EngineReport)

        Returns:
            True if collected successfully, False otherwise
        """
        if engine_id not in self.reports:
            logger.error(f"Unknown engine: {engine_id}")
            return False

        if report is None:
            logger.warning(f"Received None report from {engine_id}")
            return False

        self.reports[engine_id]["report"] = report
        self.reports[engine_id]["collected_at"] = datetime.utcnow()

        logger.info(f"Collected report from {engine_id}")

        # Check if all reports are collected
        self._check_completeness()
        return True

    def _check_completeness(self):
        """Check if all required reports have been collected."""
        self.all_collected = all(
            self.reports[engine_id]["report"] is not None for engine_id in self.reports
        )

    def get_report(self, engine_id: str) -> Any | None:
        """Get a specific report."""
        if engine_id not in self.reports:
            return None
        return self.reports[engine_id]["report"]

    def get_all_reports(self) -> dict[str, Any | None]:
        """Get all collected reports."""
        return {engine_id: data["report"] for engine_id, data in self.reports.items()}

    def get_collection_status(self) -> dict[str, Any]:
        """Get the status of report collection."""
        return {
            "all_collected": self.all_collected,
            "collected": [
                engine_id
                for engine_id, data in self.reports.items()
                if data["report"] is not None
            ],
            "missing": [
                engine_id
                for engine_id, data in self.reports.items()
                if data["report"] is None
            ],
            "collection_times": {
                engine_id: data["collected_at"]
                for engine_id, data in self.reports.items()
                if data["collected_at"] is not None
            },
        }

    def clear(self):
        """Clear all collected reports."""
        for engine_id in self.reports:
            self.reports[engine_id]["report"] = None
            self.reports[engine_id]["collected_at"] = None
        self.all_collected = False
        logger.info("Cleared all collected reports")
