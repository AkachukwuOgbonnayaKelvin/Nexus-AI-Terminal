# -*- coding: utf-8 -*-
"""GDP Collector - Collects full historical GDP data for all countries"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from macroeconomic_statistics_engine.collectors.base_collector import BaseCollector
from macroeconomic_statistics_engine.providers.base import MacroObservation
from macroeconomic_statistics_engine.providers.registry import MacroProviderRegistry


class GDPCollector(BaseCollector):
    """Collects GDP data from primary and fallback sources"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._indicator = "gdp"
        self._countries = ["US", "EU", "UK", "JP", "CH", "CA", "AU", "NZ"]
    
    def get_indicator_name(self) -> str:
        return "GDP"
    
    def get_countries(self) -> List[str]:
        return self._countries
    
    def collect(self) -> List[MacroObservation]:
        """Collect full historical GDP data for all countries"""
        self._clear_observations()
        
        # Use a wide date range to get full history
        end_date = datetime.now()
        start_date = datetime(1990, 1, 1)  # 30+ years of data
        
        for country in self.get_countries():
            print(f"Collecting GDP for {country}...")
            
            # Get providers for this country
            providers = self.registry.get_providers_for_indicator(self._indicator, country)
            
            for provider in providers:
                if provider.is_available():
                    print(f"  Using {provider.get_provider_name()} (Tier {provider.get_tier()})")
                    data = provider.get_indicator(self._indicator, country, start_date, end_date)
                    if data:
                        print(f"  Found {len(data)} observations")
                        for obs in data:
                            self._add_observation(obs)
                        break
                    else:
                        print(f"  No data from {provider.get_provider_name()}")
        
        return self._observations
    
    def get_historical_coverage(self) -> Dict[str, Any]:
        """Get historical coverage report"""
        coverage = {}
        
        for country in self.get_countries():
            country_obs = [o for o in self._observations if o.country == country]
            if country_obs:
                coverage[country] = {
                    "count": len(country_obs),
                    "first_period": min(o.period for o in country_obs),
                    "last_period": max(o.period for o in country_obs),
                    "currency": country_obs[0].currency,
                    "source": country_obs[0].source,
                    "tier": country_obs[0].source_tier
                }
            else:
                coverage[country] = {
                    "count": 0,
                    "status": "No data"
                }
        
        return coverage
