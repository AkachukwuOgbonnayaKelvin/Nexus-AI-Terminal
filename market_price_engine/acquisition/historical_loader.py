# -*- coding: utf-8 -*-
"""Historical Data Loader - Loads historical data from providers"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import sys
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.registry import ProviderRegistry
from providers.base import OHLCVData


class HistoricalDataLoader:
    """Loads historical market data from configured providers"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.registry = ProviderRegistry(config)
        self.logger = logging.getLogger(__name__)
    
    def load_historical_bars(
        self,
        symbol: str,
        timeframe: str,
        days_back: int = 80,
        provider_name: Optional[str] = None
    ) -> List[OHLCVData]:
        """Load historical bars for a symbol"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Get the provider
        if provider_name:
            provider = self.registry.get_provider(provider_name)
        else:
            # Use primary provider
            provider = self.registry.get_primary_provider()
        
        if not provider:
            print(f"No provider available for {symbol}")
            return []
        
        if not provider.is_available():
            print(f"Provider {provider.get_provider_name()} is not available")
            return []
        
        print(f"Loading {days_back} days of {timeframe} data for {symbol} from {provider.get_provider_name()}")
        
        try:
            bars = provider.get_historical_bars(symbol, timeframe, start_date, end_date)
            print(f"Loaded {len(bars)} bars for {symbol}")
            return bars
        except Exception as e:
            print(f"Error loading {symbol}: {e}")
            return []
    
    def load_historical_multi_symbol(
        self,
        symbols: List[str],
        timeframe: str = "D1",
        days_back: int = 80
    ) -> Dict[str, List[OHLCVData]]:
        """Load historical data for multiple symbols"""
        
        results = {}
        for symbol in symbols:
            results[symbol] = self.load_historical_bars(
                symbol, timeframe, days_back
            )
        return results
    
    def validate_coverage(
        self,
        symbol: str,
        timeframe: str,
        required_days: int = 80
    ) -> Dict[str, Any]:
        """Validate historical data coverage"""
        
        bars = self.load_historical_bars(symbol, timeframe, required_days)
        
        if not bars:
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "coverage": 0,
                "required_days": required_days,
                "actual_days": 0,
                "bar_count": 0,
                "status": "FAIL",
                "message": "No data available"
            }
        
        # Calculate actual days covered
        if len(bars) > 0:
            first_date = bars[0].timestamp
            last_date = bars[-1].timestamp
            actual_days = (last_date - first_date).days + 1
            
            coverage_pct = min(100, int((actual_days / required_days) * 100))
            
            status = "PASS" if coverage_pct >= 90 else "PARTIAL" if coverage_pct >= 50 else "FAIL"
            
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "coverage": coverage_pct,
                "required_days": required_days,
                "actual_days": actual_days,
                "bar_count": len(bars),
                "first_date": first_date.isoformat(),
                "last_date": last_date.isoformat(),
                "status": status,
                "message": f"{coverage_pct}% coverage ({actual_days}/{required_days} days)"
            }
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "coverage": 0,
            "required_days": required_days,
            "actual_days": 0,
            "bar_count": 0,
            "status": "FAIL",
            "message": "Insufficient data"
        }
