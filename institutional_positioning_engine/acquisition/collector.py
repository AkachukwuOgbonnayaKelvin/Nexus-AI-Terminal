"""COT Acquisition Collector – orchestrates historical and incremental collection."""

import logging
from typing import List

from institutional_positioning_engine.collectors.historical import HistoricalCollector
from institutional_positioning_engine.collectors.incremental import IncrementalCollector
from institutional_positioning_engine.dtos import UniversalCOTRecord
from institutional_positioning_engine.warehouse import COTWarehouse
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class COTCollector:
    def __init__(self, provider_manager: ProviderManager):
        self.pm = provider_manager
        self.historical = HistoricalCollector(provider_manager)
        self.incremental = IncrementalCollector(provider_manager)
        self.warehouse = COTWarehouse()

    async def collect_historical(self) -> List[UniversalCOTRecord]:
        """Collect all historical COT reports."""
        logger.info("Starting historical COT collection")
        raw_reports = await self.historical.collect_all()
        records = self._adapt_reports(raw_reports)
        logger.info(f"Collected {len(records)} historical records")
        return records

    async def collect_latest(self) -> List[UniversalCOTRecord]:
        """Collect the latest COT report."""
        logger.info("Starting incremental COT collection")
        raw_reports = await self.incremental.collect_latest()
        records = self._adapt_reports(raw_reports)
        logger.info(f"Collected {len(records)} latest records")
        return records

    async def collect_and_store(self) -> dict:
        """Collect and store all reports (historical + incremental)."""
        # Check if we have existing data
        existing = await self.warehouse.get_latest_reports(limit=1)
        if not existing:
            logger.info("No existing COT data found. Running historical collection...")
            records = await self.collect_historical()
            stored = await self._store_records(records)
            return {"historical": stored, "incremental": 0}

        # If we have data, just do incremental
        logger.info("Existing COT data found. Running incremental collection...")
        records = await self.collect_latest()
        stored = await self._store_records(records)
        return {"historical": 0, "incremental": stored}

    def _adapt_reports(self, reports: List) -> List[UniversalCOTRecord]:
        """Adapt raw reports to UniversalCOTRecord."""
        records = []
        for report in reports:
            provider_name = report.get("provider", "cftc")
            provider = self.pm.get_provider(provider_name)
            if not provider:
                continue
            adapter = self.pm.get_adapter(provider_name)
            if not adapter:
                continue
            adapted = adapter.adapt(report, provider_name)
            records.extend(adapted)
        return records

    async def _store_records(self, records: List[UniversalCOTRecord]) -> int:
        """Store records in the warehouse."""
        stored = 0
        for record in records:
            result = await self.warehouse.store(record)
            if result:
                stored += 1
        return stored
