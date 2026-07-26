"""CFTC Provider Manager – Orchestrates multiple data sources."""

import logging
from typing import Any

from institutional_positioning_engine.providers.cftc.historical import (
    HistoricalArchiveClient,
)
from institutional_positioning_engine.providers.cftc.pre_api import PREAPIClient

logger = logging.getLogger(__name__)


class CFTCProviderManager:
    """Manages CFTC data sources with automatic failover."""

    def __init__(self):
        self.pre_api = PREAPIClient()
        self.historical = HistoricalArchiveClient()
        self._sources = {
            "pre_api": self.pre_api,
            "historical": self.historical,
        }

    def get_latest_report(self) -> list[dict[str, Any]] | None:
        """Get the latest report from the best available source."""
        # Try PRE API first
        try:
            data = self.pre_api.get_latest_report()
            if data:
                logger.info("Successfully fetched latest report from PRE API")
                return data
        except Exception as e:
            logger.warning(f"PRE API failed: {e}")

        # Fallback to historical archive
        try:
            data = self.historical.get_latest_report()
            if data:
                logger.info(
                    "Successfully fetched latest report from historical archive"
                )
                return data
        except Exception as e:
            logger.warning(f"Historical archive failed: {e}")

        return None

    def get_historical_report(self, year: int) -> list[dict[str, Any]] | None:
        """Get historical reports from the best available source."""
        try:
            data = self.historical.get_year(year)
            if data:
                logger.info(f"Successfully fetched historical data for {year}")
                return data
        except Exception as e:
            logger.warning(f"Historical fetch for {year} failed: {e}")

        return None

    def health_check(self) -> dict[str, bool]:
        """Check health of all sources."""
        return {
            "pre_api": self.pre_api.health_check(),
            "historical": self.historical.health_check(),
        }
