"""COT Updater – incremental weekly updates."""

import logging
from datetime import datetime

from institutional_positioning_engine.downloader import ReportDownloader
from institutional_positioning_engine.parser import ParserFactory
from institutional_positioning_engine.runtime.state import COTRuntimeState
from institutional_positioning_engine.warehouse import COTWarehouse

logger = logging.getLogger(__name__)


class COTUpdater:
    """Incremental COT updater – downloads only the latest report."""

    def __init__(self):
        self.downloader = ReportDownloader()
        self.parser_factory = ParserFactory()
        self.warehouse = COTWarehouse()
        self.state = COTRuntimeState()

    async def update_latest(self) -> dict:
        """Download and store the latest COT report."""
        logger.info("Fetching latest COT report...")
        try:
            # Check if we already have the latest
            last_report = await self.state.get_last_report()
            # In production, we'd check if a newer report is available
            # For now, we'll just download the latest stub
            report = {
                "report_id": f"cot_{datetime.now().strftime('%Y%m%d')}",
                "url": "https://www.cftc.gov/dea/cot_latest.csv",
                "year": datetime.now().year,
                "week": datetime.now().isocalendar()[1],
            }
            self.downloader.download_report(report)
            if report.get("local_path"):
                records = self.parser_factory.parse("disaggregated", [report])
                stored = 0
                for record in records:
                    if await self.warehouse.store(record):
                        stored += 1
                await self.state.update_last_report(report["report_id"])
                return {
                    "status": "success",
                    "records": stored,
                    "report": report["report_id"],
                }
            return {"status": "error", "reason": "Download failed"}
        except Exception as e:
            logger.error(f"Update failed: {e}")
            return {"status": "error", "reason": str(e)}
