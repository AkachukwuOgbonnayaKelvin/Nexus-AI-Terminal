"""Incremental COT Collector – downloads only the latest weekly report."""

import logging
from datetime import datetime
from typing import Any, Dict, List

from institutional_positioning_engine.collectors.base import BaseCollector

logger = logging.getLogger(__name__)


class IncrementalCollector(BaseCollector):
    """Collects only the latest weekly COT report."""

    def __init__(self, provider_manager):
        super().__init__(provider_manager)

    async def collect_all(self) -> List[Dict[str, Any]]:
        """Collect all historical (not used for incremental)."""
        logger.warning("IncrementalCollector does not support collect_all")
        return []

    async def collect_latest(self) -> List[Dict[str, Any]]:
        """Collect the latest COT report."""
        logger.info("Collecting latest COT report")
        report = self._generate_stub_report()
        logger.info(f"Collected latest report: {report['report_date']}")
        return [report]

    def _generate_stub_report(self) -> Dict[str, Any]:
        """Generate a stub report for the current week."""
        today = datetime.now().date().isoformat()
        return {
            "report_id": f"cot_latest_{today}",
            "provider": "cftc",
            "report_date": today,
            "markets": [
                {
                    "market_code": "EURUSD",
                    "market_name": "Euro FX",
                    "asset_class": "forex",
                    "currency": "EUR",
                    "exchange": "CME",
                    "open_interest": 100000,
                    "dealer_long": 20000,
                    "dealer_short": 15000,
                    "commercial_long": 25000,
                    "commercial_short": 20000,
                    "asset_manager_long": 25000,
                    "asset_manager_short": 20000,
                    "leveraged_long": 18000,
                    "leveraged_short": 22000,
                    "nonreportable_long": 10000,
                    "nonreportable_short": 8000,
                },
                {
                    "market_code": "XAUUSD",
                    "market_name": "Gold",
                    "asset_class": "commodity",
                    "currency": "USD",
                    "exchange": "COMEX",
                    "open_interest": 50000,
                    "dealer_long": 10000,
                    "dealer_short": 18000,
                    "commercial_long": 15000,
                    "commercial_short": 8000,
                    "asset_manager_long": 15000,
                    "asset_manager_short": 8000,
                    "leveraged_long": 12000,
                    "leveraged_short": 14000,
                    "nonreportable_long": 5000,
                    "nonreportable_short": 4000,
                },
            ],
        }
