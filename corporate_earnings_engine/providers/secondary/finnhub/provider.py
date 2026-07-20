# -*- coding: utf-8 -*-
"""Finnhub Provider - International earnings data"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path
import os
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from corporate_earnings_engine.providers.base import EarningsProvider, EarningsObservation, FinancialStatement


class FinnhubProvider(EarningsProvider):
    """Finnhub provider for international earnings data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "finnhub"
        self.api_key = self.config.get("api_key", "") or os.getenv('FINNHUB_API_KEY', '')
        self.base_url = "https://finnhub.io/api/v1"
        self._cache = {}
        self._rate_limit_remaining = 60
        self._rate_limit_reset = 0
    
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
            "rate_limit_remaining": self._rate_limit_remaining,
            "status": "healthy" if self.is_available() else "unavailable"
        }
    
    def get_available_symbols(self) -> List[str]:
        return [
            # US
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA",
            # Europe
            "SAP", "ASML", "NOVO-B.CO", "NESN.SW", "HSBA.L",
            # Japan
            "9984.T", "6758.T", "8306.T",
            # UK
            "BP.L", "SHEL.L",
            # Canada
            "RY.TO", "TD.TO", "BNS.TO",
            # Australia
            "BHP.AX", "CBA.AX", "CSL.AX"
        ]
    
    def _check_rate_limit(self):
        """Check and respect rate limits"""
        current_time = time.time()
        if current_time < self._rate_limit_reset and self._rate_limit_remaining <= 0:
            wait_time = self._rate_limit_reset - current_time
            print(f"[Finnhub] Rate limit reached, waiting {wait_time:.1f}s...")
            time.sleep(wait_time + 1)
        return True
    
    def _update_rate_limit(self, response):
        """Update rate limit from response headers"""
        remaining = response.headers.get('X-Ratelimit-Remaining')
        reset = response.headers.get('X-Ratelimit-Reset')
        if remaining:
            self._rate_limit_remaining = int(remaining)
        if reset:
            self._rate_limit_reset = int(reset)
    
    def get_earnings(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[EarningsObservation]:
        """Get earnings data from Finnhub API"""
        if not self.is_available():
            return []
        
        self._check_rate_limit()
        
        try:
            url = f"{self.base_url}/stock/earnings"
            params = {
                "symbol": symbol,
                "token": self.api_key,
                "limit": 20
            }
            
            response = requests.get(url, params=params, timeout=30)
            self._update_rate_limit(response)
            
            if response.status_code != 200:
                print(f"[Finnhub] Error for {symbol}: {response.status_code}")
                return []
            
            data = response.json()
            
            if not data:
                return []
            
            results = []
            for item in data:
                # Use 'period' field (not 'date') from Finnhub response
                period_str = item.get("period") or item.get("date")
                if period_str:
                    try:
                        # Parse period
                        if len(period_str) == 10:  # YYYY-MM-DD
                            period_date = datetime.strptime(period_str, "%Y-%m-%d")
                        else:
                            period_date = datetime.now()
                        
                        results.append(EarningsObservation(
                            symbol=symbol,
                            company_name=symbol,
                            period=period_str,
                            period_type="quarterly",
                            actual_eps=item.get("actual"),
                            estimated_eps=item.get("estimate"),
                            actual_revenue=item.get("revenue"),
                            estimated_revenue=item.get("revenueEstimate"),
                            currency="USD",
                            fiscal_period_end=period_date,
                            announcement_date=period_date,
                            source=self.name,
                            source_tier=2,
                            quality_score=85.0,
                            provenance={
                                "surprise": item.get("surprise"),
                                "surprise_percent": item.get("surprisePercent"),
                                "year": item.get("year"),
                                "quarter": item.get("quarter")
                            }
                        ))
                    except Exception as e:
                        print(f"[Finnhub] Date parse error: {e}")
                        continue
            
            return results
            
        except Exception as e:
            print(f"[Finnhub] Error for {symbol}: {e}")
            return []
    
    def get_financial_statements(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[FinancialStatement]:
        """Get financial statements from Finnhub API"""
        if not self.is_available():
            return []
        
        try:
            url = f"{self.base_url}/stock/financials"
            params = {
                "symbol": symbol,
                "token": self.api_key,
                "statement": "income",
                "frequency": "quarterly"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            results = []
            for item in data.get("data", []):
                results.append(FinancialStatement(
                    symbol=symbol,
                    company_name=symbol,
                    period=item.get("period", ""),
                    period_type="quarterly",
                    revenue=item.get("revenue"),
                    net_income=item.get("netIncome"),
                    operating_income=item.get("operatingIncome"),
                    gross_profit=item.get("grossProfit"),
                    currency="USD",
                    source=self.name,
                    source_tier=2
                ))
            
            return results
            
        except Exception as e:
            print(f"[Finnhub] Financial statements error: {e}")
            return []
