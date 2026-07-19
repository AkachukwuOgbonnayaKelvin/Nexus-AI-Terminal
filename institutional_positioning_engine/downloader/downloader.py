"""Report Downloader – downloads reports from the catalog."""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from pathlib import Path

from institutional_positioning_engine.discovery.catalog import ReportCatalog
from institutional_positioning_engine.providers.cftc.connector import CFTCConnector

logger = logging.getLogger(__name__)


class ReportDownloader:
    """Download and archive COT reports using the catalog."""

    def __init__(self, archive_dir: str = "data/raw/cot"):
        self.connector = CFTCConnector()
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.catalog = ReportCatalog()

    def download_report(self, report: Dict[str, Any]) -> bool:
        """Download a single report from the catalog."""
        url = report.get("url")
        if not url:
            return False

        # Create destination path
        filename = report.get("filename", url.split("/")[-1])
        dest = self.archive_dir / filename
        dest.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Downloading {url} to {dest}")
        result = self.connector.download_file(url, str(dest))
        if result:
            logger.info(f"Downloaded {filename}")
            report["downloaded"] = True
            report["local_path"] = str(dest)
            self.catalog.mark_downloaded(url)
        else:
            logger.warning(f"Failed to download {url}")
        return result

    def download_pending(self, limit: int = None) -> dict:
        """Download all pending reports from the catalog."""
        pending = self.catalog.get_pending_downloads()
        if limit:
            pending = pending[:limit]

        success = 0
        failed = 0
        for report in pending:
            if self.download_report(report):
                success += 1
            else:
                failed += 1

        return {"success": success, "failed": failed, "total": len(pending)}
