"""Historical Import – One-time backfill of all CFTC archives."""

import logging
from datetime import datetime
from typing import Any

from market_positioning_warehouse.parser import ParserFactory
from market_positioning_warehouse.providers.cftc.historical_loader import (
    HistoricalLoader,
)
from market_positioning_warehouse.warehouse import Repository

logger = logging.getLogger(__name__)


class HistoricalImport:
    """One-time historical import from all CFTC archives."""

    def __init__(self):
        self.loader = HistoricalLoader()
        self.parser = ParserFactory()
        self.repository = Repository()
        self.start_year = 1986
        self.end_year = datetime.now().year

    async def run(self) -> dict[str, Any]:
        """Run the historical import."""
        logger.info(
            f"Starting historical import from {self.start_year} to {self.end_year}"
        )

        total_records = 0
        years_processed = 0

        for year in range(self.start_year, self.end_year + 1):
            try:
                raw_data = self.loader.load_year(year)
                if not raw_data:
                    logger.info(f"No data found for {year}")
                    continue

                parsed = self.parser.parse(raw_data)
                for record in parsed:
                    stored = await self.repository.store(record)
                    if stored:
                        total_records += 1

                years_processed += 1
                logger.info(f"Processed {year}: {len(parsed)} records")

            except Exception as e:
                logger.error(f"Failed to process {year}: {e}")

        logger.info(
            f"Historical import complete: {total_records} records from {years_processed} years"
        )
        return {"years_processed": years_processed, "records_inserted": total_records}
