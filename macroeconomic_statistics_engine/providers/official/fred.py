"""FRED Provider - Federal Reserve Economic Data"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Fix import path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Fix import - use relative import
from macroeconomic_statistics_engine.providers.base import (
    MacroObservation,
    MacroProvider,
)


class FREDProvider(MacroProvider):
    """FRED economic data provider"""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.name = "fred"
        self.api_key = self.config.get("api_key", "")
        self.base_url = "https://api.stlouisfed.org/fred"
        self._cache = {}

    def get_provider_name(self) -> str:
        return self.name

    def get_tier(self) -> int:
        return 1

    def is_available(self) -> bool:
        return bool(self.api_key) and REQUESTS_AVAILABLE

    def get_health(self) -> dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "has_api_key": bool(self.api_key),
            "status": "healthy" if self.is_available() else "unavailable",
        }

    def get_available_countries(self) -> list[str]:
        return ["US"]

    def get_available_indicators(self, country: str) -> list[str]:
        if country != "US":
            return []
        return [
            "gdp",
            "gdp_growth",
            "gdppot",
            "cpi",
            "core_cpi",
            "pce",
            "core_pce",
            "ppi",
            "unemployment",
            "payrolls",
            "participation_rate",
            "fed_funds_rate",
            "treasury_10y",
            "treasury_2y",
            "industrial_production",
            "capacity_utilization",
            "retail_sales",
            "consumer_confidence",
            "housing_starts",
            "existing_home_sales",
        ]

    def get_indicator(
        self,
        indicator: str,
        country: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[MacroObservation]:
        """Get a specific indicator from FRED"""
        if not self.is_available() or country != "US":
            return []

        # Map indicator to FRED series ID
        series_map = {
            "gdp": "GDP",
            "gdp_growth": "GDPC1",
            "gdppot": "GDPPOT",
            "cpi": "CPIAUCSL",
            "core_cpi": "CPILFESL",
            "pce": "PCE",
            "core_pce": "PCEPILFE",
            "ppi": "PPIACO",
            "unemployment": "UNRATE",
            "payrolls": "PAYEMS",
            "participation_rate": "CIVPART",
            "fed_funds_rate": "FEDFUNDS",
            "treasury_10y": "DGS10",
            "treasury_2y": "DGS2",
            "industrial_production": "INDPRO",
            "capacity_utilization": "TCU",
            "retail_sales": "RSXFS",
            "consumer_confidence": "UMCSENT",
            "housing_starts": "HOUST",
            "existing_home_sales": "EXHOSLUSM495S",
        }

        series_id = series_map.get(indicator)
        if not series_id:
            return []

        try:
            params = {
                "series_id": series_id,
                "api_key": self.api_key,
                "file_type": "json",
                "observation_start": start_date.strftime("%Y-%m-%d")
                if start_date
                else "1900-01-01",
                "observation_end": end_date.strftime("%Y-%m-%d")
                if end_date
                else datetime.now().strftime("%Y-%m-%d"),
            }

            url = f"{self.base_url}/series/observations"
            response = requests.get(url, params=params, timeout=30)

            if response.status_code != 200:
                print(f"FRED error: {response.status_code} - {response.text[:100]}")
                return []

            data = response.json()
            observations = data.get("observations", [])

            results = []
            for obs in observations:
                if obs.get("value") and obs["value"] != ".":
                    # Determine frequency
                    frequency = self._get_frequency(indicator)

                    results.append(
                        MacroObservation(
                            indicator=indicator,
                            country="US",
                            period=obs["date"],
                            value=float(obs["value"]),
                            unit=self._get_unit(indicator),
                            frequency=frequency,
                            source=self.name,
                            source_tier=1,
                            release_date=datetime.strptime(obs["date"], "%Y-%m-%d"),
                            vintage_date=datetime.now(),
                            revision_number=0,
                            quality_score=100.0,
                            status="official",
                        )
                    )

            return results

        except Exception as e:
            print(f"FRED error for {indicator}: {e}")
            return []

    def _get_unit(self, indicator: str) -> str:
        """Get unit for indicator"""
        unit_map = {
            "gdp": "billions",
            "gdp_growth": "percent",
            "gdppot": "billions",
            "cpi": "index",
            "core_cpi": "index",
            "pce": "index",
            "core_pce": "index",
            "ppi": "index",
            "unemployment": "percent",
            "payrolls": "thousands",
            "participation_rate": "percent",
            "fed_funds_rate": "percent",
            "treasury_10y": "percent",
            "treasury_2y": "percent",
            "industrial_production": "index",
            "capacity_utilization": "percent",
            "retail_sales": "billions",
            "consumer_confidence": "index",
            "housing_starts": "thousands",
            "existing_home_sales": "millions",
        }
        return unit_map.get(indicator, "unknown")

    def _get_frequency(self, indicator: str) -> str:
        """Get frequency for indicator"""
        freq_map = {
            "gdp": "quarterly",
            "gdp_growth": "quarterly",
            "gdppot": "quarterly",
            "cpi": "monthly",
            "core_cpi": "monthly",
            "pce": "monthly",
            "core_pce": "monthly",
            "ppi": "monthly",
            "unemployment": "monthly",
            "payrolls": "monthly",
            "participation_rate": "monthly",
            "fed_funds_rate": "daily",
            "treasury_10y": "daily",
            "treasury_2y": "daily",
            "industrial_production": "monthly",
            "capacity_utilization": "monthly",
            "retail_sales": "monthly",
            "consumer_confidence": "monthly",
            "housing_starts": "monthly",
            "existing_home_sales": "monthly",
        }
        return freq_map.get(indicator, "unknown")
