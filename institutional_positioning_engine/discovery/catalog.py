"""Report Catalog – stores and manages discovered reports."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from pathlib import Path

logger = logging.getLogger(__name__)


class ReportCatalog:
    """Persistent catalog of discovered COT reports."""

    def __init__(self, catalog_path: str = "data/cot_catalog.json"):
        self.catalog_path = Path(catalog_path)
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        self.reports = self._load_catalog()

    def _load_catalog(self) -> List[Dict[str, Any]]:
        """Load catalog from file."""
        if self.catalog_path.exists():
            try:
                with open(self.catalog_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load catalog: {e}")
                return []
        return []

    def _save_catalog(self) -> None:
        """Save catalog to file."""
        try:
            with open(self.catalog_path, "w") as f:
                json.dump(self.reports, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save catalog: {e}")

    def add_report(self, report: Dict[str, Any]) -> None:
        """Add a report to the catalog."""
        for existing in self.reports:
            if existing.get("url") == report.get("url"):
                return
        self.reports.append(report)
        self._save_catalog()

    def add_reports(self, reports: List[Dict[str, Any]]) -> None:
        """Add multiple reports to the catalog."""
        for report in reports:
            self.add_report(report)

    def get_pending_downloads(self) -> List[Dict[str, Any]]:
        """Get reports that haven't been downloaded yet."""
        return [r for r in self.reports if not r.get("downloaded")]

    def get_pending_parses(self) -> List[Dict[str, Any]]:
        """Get reports that have been downloaded but not parsed."""
        return [r for r in self.reports if r.get("downloaded") and not r.get("parsed")]

    def mark_downloaded(self, url: str) -> None:
        """Mark a report as downloaded."""
        for report in self.reports:
            if report.get("url") == url:
                report["downloaded"] = True
                report["downloaded_at"] = datetime.now().isoformat()
                self._save_catalog()
                break

    def mark_parsed(self, url: str) -> None:
        """Mark a report as parsed."""
        for report in self.reports:
            if report.get("url") == url:
                report["parsed"] = True
                report["parsed_at"] = datetime.now().isoformat()
                self._save_catalog()
                break

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all reports."""
        return self.reports

    def get_by_report_type(self, report_type: str) -> List[Dict[str, Any]]:
        """Get reports by type."""
        return [r for r in self.reports if r.get("report_type") == report_type]

    def get_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Get reports by date."""
        return [r for r in self.reports if r.get("date") == date]

    def get_counts(self) -> Dict[str, int]:
        """Get catalog statistics."""
        return {
            "total": len(self.reports),
            "downloaded": len([r for r in self.reports if r.get("downloaded")]),
            "parsed": len([r for r in self.reports if r.get("parsed")]),
            "pending_download": len(self.get_pending_downloads()),
            "pending_parse": len(self.get_pending_parses()),
        }
