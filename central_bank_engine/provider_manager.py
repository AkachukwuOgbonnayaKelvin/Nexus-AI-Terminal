"""Provider Manager – orchestrates collectors for all central banks."""

import logging
from typing import Any, Dict, List

from central_bank_engine.collectors import BaseCollector
from central_bank_engine.registry import get_all_banks

logger = logging.getLogger(__name__)


class ProviderManager:
    """Manages all collectors and their schedules."""

    def __init__(self):
        self.collectors: List[BaseCollector] = []
        self.banks = get_all_banks()

    def register_collector(self, collector: BaseCollector) -> None:
        """Register a collector."""
        self.collectors.append(collector)
        logger.info(f"Registered collector: {collector.name} for {collector.bank_id}")

    def get_collectors_by_bank(self, bank_id: str) -> List[BaseCollector]:
        """Get all collectors for a specific bank."""
        return [c for c in self.collectors if c.bank_id == bank_id]

    def get_collector_statuses(self) -> Dict[str, Any]:
        """Get status of all collectors."""
        return {c.name: c.get_status() for c in self.collectors}

    async def run_all_collectors(self) -> List[Dict[str, Any]]:
        """Run all collectors and return combined events."""
        all_events = []
        for collector in self.collectors:
            try:
                events = await collector.collect()
                all_events.extend(events)
                collector.log_success()
            except Exception as e:
                collector.log_error(e)
        return all_events

    async def run_collector(self, collector_name: str) -> List[Dict[str, Any]]:
        """Run a specific collector by name."""
        for collector in self.collectors:
            if collector.name == collector_name:
                try:
                    events = await collector.collect()
                    collector.log_success()
                    return events
                except Exception as e:
                    collector.log_error(e)
                    return []
        return []
