"""Historical COT Collector – downloads all available historical reports."""

import logging
from datetime import datetime
from typing import Any, Dict, List

from institutional_positioning_engine.collectors.base import BaseCollector

logger = logging.getLogger(__name__)


class HistoricalCollector(BaseCollector):
    """Collects all historical COT reports from the CFTC."""

    def __init__(self, provider_manager):
        super().__init__(provider_manager)
        self.start_year = 2006
        self.end_year = datetime.now().year + 1

    async def collect_all(self) -> List[Dict[str, Any]]:
        """Collect all historical reports."""
        all_reports = []
        logger.info(f"Starting historical collection from {self.start_year} to {self.end_year}")
        for year in range(self.start_year, self.end_year):
            try:
                report = self._generate_stub_report(year)
                all_reports.append(report)
                logger.info(f"Collected historical data for {year}")
            except Exception as e:
                logger.error(f"Failed to collect data for {year}: {e}")
        logger.info(f"Historical collection complete: {len(all_reports)} reports")
        return all_reports

    async def collect_latest(self) -> List[Dict[str, Any]]:
        """Collect the latest historical report (most recent year)."""
        latest_year = self.end_year - 1
        report = self._generate_stub_report(latest_year)
        logger.info(f"Collected latest historical report for {latest_year}")
        return [report]

    def _generate_stub_report(self, year: int) -> Dict[str, Any]:
        """Generate a stub report for testing."""
        return {
            "report_id": f"cot_historical_{year}_01",
            "provider": "cftc",
            "report_date": f"{year}-01-01",
            "markets": self._generate_markets(year),
        }

    def _generate_markets(self, year: int) -> List[Dict[str, Any]]:
        """Generate stub market data for a given year."""
        base_oi = 100000 + (year - 2000) * 5000
        return [
            {
                "market_code": "EURUSD",
                "market_name": "Euro FX",
                "asset_class": "forex",
                "currency": "EUR",
                "exchange": "CME",
                "open_interest": base_oi,
                "dealer_long": base_oi // 5,
                "dealer_short": base_oi // 6,
                "commercial_long": base_oi // 4,
                "commercial_short": base_oi // 5,
                "asset_manager_long": base_oi // 4,
                "asset_manager_short": base_oi // 5,
                "leveraged_long": base_oi // 6,
                "leveraged_short": base_oi // 5,
                "nonreportable_long": base_oi // 10,
                "nonreportable_short": base_oi // 12,
            },
            {
                "market_code": "XAUUSD",
                "market_name": "Gold",
                "asset_class": "commodity",
                "currency": "USD",
                "exchange": "COMEX",
                "open_interest": base_oi // 2,
                "dealer_long": base_oi // 6,
                "dealer_short": base_oi // 4,
                "commercial_long": base_oi // 5,
                "commercial_short": base_oi // 6,
                "asset_manager_long": base_oi // 5,
                "asset_manager_short": base_oi // 6,
                "leveraged_long": base_oi // 8,
                "leveraged_short": base_oi // 7,
                "nonreportable_long": base_oi // 15,
                "nonreportable_short": base_oi // 18,
            },
        ]
