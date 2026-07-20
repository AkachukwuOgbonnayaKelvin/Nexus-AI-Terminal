"""Weekly Scheduler – Runs every Friday."""

import logging
from datetime import datetime

from market_positioning_warehouse.parser import ParserFactory
from market_positioning_warehouse.providers.cftc.weekly_loader import WeeklyLoader
from market_positioning_warehouse.warehouse import Repository

logger = logging.getLogger(__name__)


class WeeklyScheduler:
    """Weekly update scheduler for CFTC reports."""

    def __init__(self):
        self.loader = WeeklyLoader()
        self.parser = ParserFactory()
        self.repository = Repository()
        self.last_run = None

    async def run(self) -> dict:
        """Run the weekly update."""
        today = datetime.now()

        if today.weekday() != 4:
            return {"status": "skipped", "reason": "Not Friday"}

        if self.last_run and (today - self.last_run).days < 7:
            return {"status": "skipped", "reason": "Already ran this week"}

        logger.info("Running weekly COT update...")

        try:
            raw_data = self.loader.load_current_week()
            if not raw_data:
                return {"status": "failed", "reason": "No data received"}

            parsed = self.parser.parse(raw_data)
            stored = 0
            for record in parsed:
                if await self.repository.store(record):
                    stored += 1

            self.last_run = today
            logger.info(f"Weekly update complete: {stored} records stored")
            return {"status": "success", "records": stored}

        except Exception as e:
            logger.error(f"Weekly update failed: {e}")
            return {"status": "error", "error": str(e)}
