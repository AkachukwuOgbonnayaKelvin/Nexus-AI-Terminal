"""Historical Backfill – imports all available historical COT data."""

import logging
from typing import Any, Dict

from institutional_positioning_engine.discovery import ReportDiscovery
from institutional_positioning_engine.downloader import ReportDownloader
from institutional_positioning_engine.parser import COTParser
from institutional_positioning_engine.warehouse import COTWarehouse

logger = logging.getLogger(__name__)


class HistoricalBackfill:
    """Run one-time historical backfill of all COT reports."""

    def __init__(self):
        self.discovery = ReportDiscovery()
        self.downloader = ReportDownloader()
        self.parser = COTParser()
        self.warehouse = COTWarehouse()

    async def run(self, limit: int = None) -> Dict[str, Any]:
        """Execute historical backfill."""
        logger.info("Starting historical backfill...")
        reports = self.discovery.discover_all()
        logger.info(f"Discovered {len(reports)} reports")

        if limit:
            reports = reports[:limit]

        total_records = 0
        processed = 0
        for report in reports:
            if not report.get("downloaded"):
                self.downloader.download_report(report)
            if report.get("local_path"):
                records = self.parser.parse_file(report["local_path"])
                for record in records:
                    await self.warehouse.store(record)
                    total_records += 1
                processed += 1
                if processed % 10 == 0:
                    logger.info(f"Processed {processed} reports, {total_records} records")

        markets = self.parser.get_discovered_markets()
        for code, info in markets.items():
            await self.warehouse.register_market(info)

        return {
            "reports_processed": processed,
            "records_inserted": total_records,
            "markets_discovered": len(markets),
        }
