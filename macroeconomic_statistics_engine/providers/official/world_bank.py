# -*- coding: utf-8 -*-
"""World Bank Provider - Full historical series with proper pagination"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from macroeconomic_statistics_engine.providers.base import MacroProvider, MacroObservation


class WorldBankProvider(MacroProvider):
    """World Bank data provider with full historical series"""
    
    # Country codes mapping
    COUNTRY_CODES = {
        "US": "USA",
        "EU": "EUU",
        "UK": "GBR",
        "JP": "JPN",
        "CH": "CHE",
        "CA": "CAN",
        "AU": "AUS",
        "NZ": "NZL",
        "DE": "DEU",
        "FR": "FRA",
        "IT": "ITA",
        "ES": "ESP",
        "CN": "CHN",
        "IN": "IND",
        "BR": "BRA",
        "NG": "NGA"
    }
    
    CURRENCY_MAP = {
        "US": "USD",
        "EU": "EUR",
        "UK": "GBP",
        "JP": "JPY",
        "CH": "CHF",
        "CA": "CAD",
        "AU": "AUD",
        "NZ": "NZD",
        "NG": "NGN"
    }
    
    INDICATOR_MAP = {
        "gdp": {
            "code": "NY.GDP.MKTP.CD",
            "unit": "current_usd",
            "description": "GDP (current US$)"
        },
        "gdp_growth": {
            "code": "NY.GDP.MKTP.KD.ZG",
            "unit": "percent",
            "description": "GDP growth (annual %)"
        },
        "gdp_per_capita": {
            "code": "NY.GDP.PCAP.CD",
            "unit": "current_usd",
            "description": "GDP per capita (current US$)"
        },
        "inflation": {
            "code": "FP.CPI.TOTL.ZG",
            "unit": "percent",
            "description": "Inflation, consumer prices (annual %)"
        },
        "unemployment": {
            "code": "SL.UEM.TOTL.ZS",
            "unit": "percent",
            "description": "Unemployment, total (% of total labor force)"
        },
        "population": {
            "code": "SP.POP.TOTL",
            "unit": "persons",
            "description": "Population, total"
        }
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "world_bank"
        self.base_url = "https://api.worldbank.org/v2"
        self._cache = {}
    
    def get_provider_name(self) -> str:
        return self.name
    
    def get_tier(self) -> int:
        return 2
    
    def is_available(self) -> bool:
        return REQUESTS_AVAILABLE
    
    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "status": "healthy" if self.is_available() else "unavailable"
        }
    
    def get_available_countries(self) -> List[str]:
        return list(self.COUNTRY_CODES.keys())
    
    def get_available_indicators(self, country: str) -> List[str]:
        return list(self.INDICATOR_MAP.keys())
    
    def get_currency(self, country: str) -> str:
        return self.CURRENCY_MAP.get(country, "USD")
    
    def get_indicator(
        self,
        indicator: str,
        country: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[MacroObservation]:
        """Get full historical indicator data from World Bank API"""
        if not self.is_available():
            return []
        
        indicator_info = self.INDICATOR_MAP.get(indicator)
        if not indicator_info:
            return []
        
        indicator_code = indicator_info["code"]
        country_code = self.COUNTRY_CODES.get(country)
        if not country_code:
            return []
        
        all_observations = []
        page = 1
        
        try:
            while True:
                # Build URL with pagination
                url = f"{self.base_url}/country/{country_code}/indicator/{indicator_code}"
                params = {
                    "format": "json",
                    "per_page": 1000,
                    "page": page
                }
                
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code != 200:
                    break
                
                data = response.json()
                
                if not data or len(data) < 2:
                    break
                
                # Check metadata
                metadata = data[0]
                total_pages = int(metadata.get("pages", 1))
                observations = data[1]
                
                if not observations:
                    break
                
                # Process ALL observations (not just one)
                for obs in observations:
                    if obs.get("value") is not None and obs["value"] != "":
                        date_str = obs.get("date", "")
                        if date_str:
                            try:
                                if len(date_str) == 4:
                                    frequency = "annual"
                                    period = f"{date_str}-01-01"
                                    release_date = datetime.strptime(date_str, "%Y")
                                elif len(date_str) == 7:
                                    frequency = "monthly"
                                    period = f"{date_str}-01"
                                    release_date = datetime.strptime(date_str, "%Y-%m")
                                else:
                                    frequency = "annual"
                                    period = date_str
                                    release_date = datetime.now()
                                
                                # Check date range
                                if start_date and release_date < start_date:
                                    continue
                                if end_date and release_date > end_date:
                                    continue
                                
                                currency = self.get_currency(country)
                                
                                all_observations.append(MacroObservation(
                                    indicator=indicator,
                                    country=country,
                                    period=period,
                                    value=float(obs["value"]),
                                    unit=indicator_info["unit"],
                                    currency=currency,
                                    frequency=frequency,
                                    source=self.name,
                                    source_tier=2,
                                    release_date=release_date,
                                    vintage_date=datetime.now(),
                                    revision_number=0,
                                    quality_score=95.0,
                                    status="secondary",
                                    metadata={
                                        "indicator_code": indicator_code,
                                        "indicator_description": indicator_info["description"]
                                    }
                                ))
                            except (ValueError, TypeError):
                                continue
                
                # Check if we need to continue pagination
                if page >= total_pages:
                    break
                
                page += 1
                time.sleep(0.1)  # Small delay to avoid rate limits
            
            return all_observations
            
        except Exception as e:
            print(f"[DEBUG] World Bank error: {e}")
            return all_observations  # Return what we have
