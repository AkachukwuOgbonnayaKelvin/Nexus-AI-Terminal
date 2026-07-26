"""Market Price Engine – uses ProviderManager to fetch and publish data to NDIP."""

import asyncio
import logging
from typing import Any

from ndip.acquisition.collector import AcquisitionCollector
from providers.provider_manager import ProviderManager

logger = logging.getLogger(__name__)


class MarketPriceEngine:
    """Market Price Engine – collects and publishes price data."""

    def __init__(self, provider_manager: ProviderManager):
        self.provider_manager = provider_manager
        self.collector = AcquisitionCollector()
        self.is_running = False
        self.symbols: list[str] = []
        self.interval_seconds: int = 60

    def set_symbols(self, symbols: list[str]) -> None:
        """Set the list of symbols to track."""
        self.symbols = symbols

    def set_interval(self, seconds: int) -> None:
        """Set collection interval in seconds."""
        self.interval_seconds = seconds

    async def collect_once(self) -> dict[str, Any]:
        """Run a single collection cycle."""
        results = {}
        for symbol in self.symbols:
            logger.info(f"Fetching {symbol}...")
            transport = self.provider_manager.get_price(symbol)
            if transport is None:
                results[symbol] = {
                    "status": "failed",
                    "error": "No data from providers",
                }
                continue
            # Convert transport to dict for NDIP
            data = transport.to_dict()
            # Ingest into NDIP
            result = await self.collector.ingest(transport.source, data)
            results[symbol] = result
        return results

    async def start(self) -> None:
        """Start the engine with scheduled collection."""
        self.is_running = True
        logger.info(f"Market Price Engine started. Interval: {self.interval_seconds}s")
        while self.is_running:
            await self.collect_once()
            await asyncio.sleep(self.interval_seconds)

    def stop(self) -> None:
        """Stop the engine."""
        self.is_running = False
        logger.info("Market Price Engine stopped.")
