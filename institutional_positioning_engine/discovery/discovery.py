"""Report Discovery – find all available CFTC reports."""

import logging
from datetime import datetime, timedelta
from typing import Any

from institutional_positioning_engine.providers.cftc.connector import CFTCConnector

logger = logging.getLogger(__name__)


class ReportDiscovery:
    """Discover all available COT reports from CFTC."""

    def __init__(self):
        self.connector = CFTCConnector()
        self.report_types = [
            "disaggregated",
            "legacy_futures",
            "legacy_futures_options",
            "tff",
            "supplemental",
        ]

    def discover_all(self) -> list[dict[str, Any]]:
        """Discover all available reports."""
        reports = []
        # In production, this would query CFTC's directory
        # For now, we'll generate the structure
        current_year = datetime.now().year
        for year in range(1995, current_year + 1):
            for week in range(1, 53):
                report = {
                    "report_id": f"cot_{year}_w{week:02d}",
                    "year": year,
                    "week": week,
                    "report_date": self._week_to_date(year, week),
                    "url": f"https://www.cftc.gov/dea/history/cot_{year}_{week:02d}.csv",
                    "report_type": "disaggregated",
                }
                reports.append(report)
        logger.info(f"Discovered {len(reports)} reports")
        return reports

    def _week_to_date(self, year: int, week: int) -> str:
        """Convert year and week to date."""
        try:
            first_day = datetime(year, 1, 1)
            days_to_add = (week - 1) * 7
            date = first_day + timedelta(days=days_to_add)
            return date.strftime("%Y-%m-%d")
        except Exception:
            return f"{year}-01-01"
