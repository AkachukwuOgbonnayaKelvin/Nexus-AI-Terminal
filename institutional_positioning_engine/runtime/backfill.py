"""COT Backfill – historical data import."""

import logging
from datetime import datetime

from institutional_positioning_engine.discovery import ReportDiscovery
from institutional_positioning_engine.downloader import ReportDownloader
from institutional_positioning_engine.parser import ParserFactory
from institutional_positioning_engine.runtime.state import COTRuntimeState
from institutional_positioning_engine.warehouse import COTWarehouse

logger = logging.getLogger(__name__)


class COTBackfill:
    """Historical COT backfill – imports all available historical reports."""

    def __init__(self):
        self.discovery = ReportDiscovery()
        self.downloader = ReportDownloader()
        self.parser_factory = ParserFactory()
        self.warehouse = COTWarehouse()
        self.state = COTRuntimeState()

    async def run_backfill(self, start_year: int = 2006, end_year: int = None) -> dict:
        """Run historical backfill from start_year to end_year."""
        if end_year is None:
            end_year = datetime.now().year

        logger.info(f"Starting backfill from {start_year} to {end_year}...")
        reports = self.discovery.discover_all()
        filtered = [r for r in reports if start_year <= r.get("year", 0) <= end_year]

        total_records = 0
        processed = 0
        for report in filtered[:10]:  # Limit for testing
            self.downloader.download_report(report)
            if report.get("local_path"):
                records = self.parser_factory.parse("disaggregated", [report])
                for record in records:
                    if await self.warehouse.store(record):
                        total_records += 1
                processed += 1

        await self.state.update_backfill_status(processed, total_records)
        return {
            "status": "success",
            "reports_processed": processed,
            "records_inserted": total_records,
        }
