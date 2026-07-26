"""Earnings Collector - Collects earnings data from multiple sources"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from corporate_earnings_engine.providers.base import EarningsObservation
from corporate_earnings_engine.providers.registry import ProviderRegistry


class EarningsCollector:
    """Collects earnings data from primary and secondary sources"""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.registry = ProviderRegistry(config)
        self._observations: list[EarningsObservation] = []

    def collect(self, symbols: list[str] | None = None) -> list[EarningsObservation]:
        """Collect earnings data for symbols"""
        self._observations = []

        if symbols is None:
            # Get symbols from primary provider
            primary = self.registry.get_primary_provider()
            if primary:
                symbols = primary.get_available_symbols()

        if not symbols:
            return []

        for symbol in symbols:
            observations = self._collect_for_symbol(symbol)
            self._observations.extend(observations)

        return self._observations

    def _collect_for_symbol(self, symbol: str) -> list[EarningsObservation]:
        """Collect earnings for a single symbol with failover"""

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 5)  # 5 years of data

        # Try Tier 1 providers first
        tier1_providers = self.registry.get_providers_by_tier(1)
        for provider in tier1_providers:
            if provider.is_available():
                data = provider.get_earnings(symbol, start_date, end_date)
                if data:
                    return data

        # Try Tier 2 providers
        tier2_providers = self.registry.get_providers_by_tier(2)
        for provider in tier2_providers:
            if provider.is_available():
                data = provider.get_earnings(symbol, start_date, end_date)
                if data:
                    return data

        return []

    def get_observations(self) -> list[EarningsObservation]:
        return self._observations
