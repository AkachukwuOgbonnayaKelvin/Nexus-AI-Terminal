"""Automated COT Scheduler – Runs independently but integrates with DAR."""

import asyncio
import logging
from datetime import datetime

from institutional_positioning_engine.parser import ParserFactory
from institutional_positioning_engine.providers.cftc.provider_manager import CFTCProviderManager
from institutional_positioning_engine.publication import COTPublisher
from institutional_positioning_engine.warehouse import COTWarehouse

logger = logging.getLogger(__name__)


class AutomatedCOTScheduler:
    """Fully automated COT scheduler integrated with DAR."""

    def __init__(self):
        self.provider_manager = CFTCProviderManager()
        self.warehouse = COTWarehouse()
        self.parser_factory = ParserFactory()
        self.publisher = COTPublisher()
        self.running = False
        self.last_run_date = None
        self.backfill_complete = False

    async def run_once(self) -> dict:
        """Run a single cycle (called by DAR)."""
        logger.info("COT Engine cycle started")

        try:
            # Check if backfill is needed
            if not self.backfill_complete:
                has_data = await self.warehouse.has_data()
                if not has_data:
                    logger.info("No data found. Starting backfill...")
                    await self._perform_backfill()
                    self.backfill_complete = True
                    return {"status": "backfill_complete"}

            # Check if it's Friday (release day)
            now = datetime.now()
            if now.weekday() == 4:  # Friday
                if self.last_run_date != now.date():
                    logger.info("Processing weekly COT update...")
                    result = await self._process_weekly_update()
                    self.last_run_date = now.date()
                    return result
                else:
                    return {"status": "idle", "message": "Already ran today"}
            else:
                return {"status": "idle", "message": "Not Friday"}

        except Exception as e:
            logger.error(f"COT Engine cycle failed: {e}")
            return {"status": "error", "error": str(e)}

    async def _process_weekly_update(self) -> dict:
        """Process the weekly COT update."""
        try:
            data = self.provider_manager.get_latest_report()
            if not data:
                logger.warning("No data received from CFTC")
                return {"status": "failed", "reason": "No data"}

            parsed = self.parser_factory.parse("disaggregated", data)
            stored_count = 0
            for record in parsed:
                if await self.warehouse.store(record):
                    stored_count += 1

            if stored_count > 0:
                await self.publisher.publish(parsed)
                logger.info(f"Successfully processed {stored_count} COT records")
                return {"status": "success", "records": stored_count}
            else:
                logger.warning("No records stored")
                return {"status": "failed", "reason": "No records stored"}

        except Exception as e:
            logger.error(f"Weekly update failed: {e}")
            return {"status": "error", "error": str(e)}

    async def _perform_backfill(self) -> dict:
        """Perform historical backfill."""
        logger.info("Performing historical backfill...")

        years = range(2006, datetime.now().year + 1)
        total_stored = 0

        for year in years:
            try:
                data = self.provider_manager.get_historical_report(year)
                if data:
                    parsed = self.parser_factory.parse("disaggregated", data)
                    for record in parsed:
                        if await self.warehouse.store(record):
                            total_stored += 1
                    logger.info(f"Backfilled {len(parsed)} records for {year}")
                else:
                    logger.info(f"No data found for {year}")
            except Exception as e:
                logger.error(f"Backfill failed for {year}: {e}")

        logger.info(f"Historical backfill complete. Total records: {total_stored}")
        return {"status": "backfill_complete", "records": total_stored}

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        logger.info("Scheduler stopped")
