# -*- coding: utf-8 -*-
"""IMF Provider - International Monetary Fund Data"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from macroeconomic_statistics_engine.providers.base import (
    MacroProvider,
    MacroObservation,
)


class IMFProvider(MacroProvider):
    """IMF data provider for cross-country macroeconomic data"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "imf"
        self.base_url = "http://dataservices.imf.org"
        self._cache = {}

    def get_provider_name(self) -> str:
        return self.name

    def get_tier(self) -> int:
        return 2  # Tier 2 - International official source

    def is_available(self) -> bool:
        return REQUESTS_AVAILABLE

    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "status": "healthy" if self.is_available() else "unavailable",
        }

    def get_available_countries(self) -> List[str]:
        """Return major countries for which IMF has data"""
        return [
            "US",
            "EU",
            "UK",
            "JP",
            "CH",
            "CA",
            "AU",
            "NZ",
            "DE",
            "FR",
            "IT",
            "ES",
            "KR",
            "CN",
            "IN",
            "BR",
        ]

    def get_available_indicators(self, country: str) -> List[str]:
        """Get available indicators for a country"""
        return [
            "gdp",
            "gdp_growth",
            "inflation",
            "unemployment",
            "current_account",
            "government_debt",
            "population",
        ]

    def get_indicator(
        self,
        indicator: str,
        country: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[MacroObservation]:
        """Get indicator data from IMF - simplified implementation"""

        # IMF API is complex with SDMX. For now, return empty.
        # Full implementation would use IMF's SDMX API.

        return []
