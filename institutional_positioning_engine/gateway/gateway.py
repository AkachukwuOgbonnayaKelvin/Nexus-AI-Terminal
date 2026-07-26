"""COT Gateway – exposes raw COT data to consumers."""

import logging
from typing import Any

from institutional_positioning_engine.warehouse import COTWarehouse

logger = logging.getLogger(__name__)


class COTGateway:
    def __init__(self, warehouse: COTWarehouse | None = None):
        self.warehouse = warehouse or COTWarehouse()

    async def get_latest_report(self, market_code: str | None = None) -> dict[str, Any]:
        """Get the latest COT report."""
        if market_code:
            latest = await self.warehouse.get_latest_positions(market_code)
            return {"market_code": market_code, "positions": latest}
        reports = await self.warehouse.get_latest_reports(limit=1)
        return reports[0] if reports else {}

    async def get_report(self, report_id: str) -> dict[str, Any] | None:
        """Get a specific report by ID."""
        return await self.warehouse.get_report(report_id)

    async def get_market_history(
        self, market_code: str, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Get historical positions for a market."""
        return await self.warehouse.get_market_history(market_code, limit)

    async def get_reports_between(
        self, start_date: str, end_date: str
    ) -> list[dict[str, Any]]:
        """Get reports between two dates."""
        return await self.warehouse.get_reports_between(start_date, end_date)

    async def get_latest_positions(self, market_code: str) -> list[dict[str, Any]]:
        """Get the latest positions for a market."""
        return await self.warehouse.get_latest_positions(market_code)

    async def get_available_markets(self) -> list[str]:
        """Get all available markets."""
        return await self.warehouse.get_available_markets()

    async def get_provider_status(self) -> dict[str, Any]:
        """Get provider health status."""
        return {"status": "healthy", "provider": "cftc"}
