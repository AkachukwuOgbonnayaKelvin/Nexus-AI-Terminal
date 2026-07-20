# -*- coding: utf-8 -*-
"""Financial Modeling Prep Provider - Normalized financial data API"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from corporate_earnings_engine.providers.base import EarningsProvider, EarningsObservation, FinancialStatement


class FMPProvider(EarningsProvider):
    """Financial Modeling Prep data provider"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "financial_modeling_prep"
        self.api_key = self.config.get("api_key", "")
        self.base_url = "https://financialmodelingprep.com/api/v3"
        self._cache = {}
    
    def get_provider_name(self) -> str:
        return self.name
    
    def get_tier(self) -> int:
        return 2
    
    def is_available(self) -> bool:
        return bool(self.api_key) and REQUESTS_AVAILABLE
    
    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "has_api_key": bool(self.api_key),
            "status": "healthy" if self.is_available() else "unavailable"
        }
    
    def get_available_symbols(self) -> List[str]:
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "BAC", "WMT"]
    
    def get_earnings(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[EarningsObservation]:
        """Get earnings data from FMP API"""
        if not self.is_available():
            return []
        
        try:
            url = f"{self.base_url}/historical/earning_calendar/{symbol}"
            params = {
                "apikey": self.api_key,
                "limit": 20
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            results = []
            for item in data:
                if item.get("date"):
                    results.append(EarningsObservation(
                        symbol=symbol,
                        company_name=symbol,
                        period=item.get("date", ""),
                        period_type="quarterly",
                        actual_eps=item.get("epsActual"),
                        estimated_eps=item.get("epsEstimate"),
                        actual_revenue=item.get("revenueActual"),
                        estimated_revenue=item.get("revenueEstimate"),
                        currency="USD",
                        announcement_date=datetime.strptime(item.get("date", "2000-01-01"), "%Y-%m-%d"),
                        source=self.name,
                        source_tier=2,
                        quality_score=90.0
                    ))
            
            return results
            
        except Exception as e:
            print(f"FMP error for {symbol}: {e}")
            return []
    
    def get_financial_statements(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[FinancialStatement]:
        """Get financial statements from FMP API"""
        return []
