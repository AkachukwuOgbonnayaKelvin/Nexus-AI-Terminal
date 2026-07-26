"""CPI Collector - Collects CPI data from multiple sources and countries"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from macroeconomic_statistics_engine.collectors.base_collector import BaseCollector
from macroeconomic_statistics_engine.providers.base import MacroObservation


class CPICollector(BaseCollector):
    """Collects CPI data from primary and fallback sources"""

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self._indicator = "cpi"
        self._countries = ["US", "EU", "UK", "JP", "CH", "CA", "AU", "NZ"]

    def get_indicator_name(self) -> str:
        return "CPI"

    def get_countries(self) -> list[str]:
        return self._countries

    def collect(self) -> list[MacroObservation]:
        """Collect CPI data for all countries"""
        self._clear_observations()

        for country in self.get_countries():
            observations = self._collect_for_country(country)
            for obs in observations:
                self._add_observation(obs)

        return self._observations

    def _collect_for_country(self, country: str) -> list[MacroObservation]:
        """Collect CPI data for a specific country with failover"""

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 5)

        providers = self.registry.get_providers_for_indicator(self._indicator, country)

        for provider in providers:
            if provider.is_available():
                data = provider.get_indicator(
                    self._indicator, country, start_date, end_date
                )
                if data:
                    return data

        return []
