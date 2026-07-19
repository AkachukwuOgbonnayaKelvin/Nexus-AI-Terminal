# -*- coding: utf-8 -*-
"""Yahoo Finance Provider - Historical market data"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False
    print("Warning: yfinance not installed. Install with: pip install yfinance")

from providers.base import MarketDataProvider, OHLCVData


class YahooFinanceProvider(MarketDataProvider):
    """Yahoo Finance historical data provider"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = "yahoo_finance"
        self._cache = {}
    
    def get_provider_name(self) -> str:
        return self.name
    
    def is_available(self) -> bool:
        return YF_AVAILABLE
    
    def get_health(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "cache_size": len(self._cache),
            "status": "healthy" if self.is_available() else "unavailable"
        }
    
    def get_available_symbols(self) -> List[str]:
        """Return common symbols available on Yahoo Finance"""
        return [
            "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X",
            "USDCAD=X", "AUDUSD=X", "NZDUSD=X",
            "GC=F", "SI=F", "CL=F", "NG=F",
            "^GSPC", "^IXIC", "^DJI", "^FTSE", "^GDAXI",
            "BTC-USD", "ETH-USD"
        ]
    
    def get_current_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current quote from Yahoo Finance"""
        if not self.is_available():
            return None
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                "symbol": symbol,
                "bid": info.get("bid", 0),
                "ask": info.get("ask", 0),
                "last": info.get("regularMarketPrice", 0),
                "timestamp": datetime.now(),
                "source": self.name
            }
        except Exception as e:
            print(f"Yahoo quote error for {symbol}: {e}")
            return None
    
    def get_historical_bars(
        self,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[OHLCVData]:
        """Get historical OHLCV data from Yahoo Finance"""
        if not self.is_available():
            return []
        
        try:
            # Map timeframe to yfinance interval
            interval_map = {
                "M1": "1m", "M5": "5m", "M15": "15m",
                "M30": "30m", "H1": "60m", "H4": "1h",
                "D1": "1d", "W1": "1wk", "MN1": "1mo"
            }
            
            interval = interval_map.get(timeframe, "1d")
            
            # Fetch data
            ticker = yf.Ticker(symbol)
            data = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
            
            if data.empty:
                return []
            
            # Convert to OHLCVData
            bars = []
            for idx, row in data.iterrows():
                bars.append(OHLCVData(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=idx.to_pydatetime(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=float(row["Volume"]) if "Volume" in row else None,
                    source=self.name,
                    quality_score=98.0
                ))
            
            return bars
            
        except Exception as e:
            print(f"Yahoo historical error for {symbol}: {e}")
            return []
