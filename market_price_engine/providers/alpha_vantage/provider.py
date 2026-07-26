"""Alpha Vantage Provider - API-based market data"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from providers.base import MarketDataProvider, OHLCVData


class AlphaVantageProvider(MarketDataProvider):
    """Alpha Vantage API provider"""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.name = "alpha_vantage"
        self.api_key = self.config.get("api_key", "")
        self.base_url = "https://www.alphavantage.co/query"
        self._cache = {}

    def get_provider_name(self) -> str:
        return self.name

    def is_available(self) -> bool:
        return bool(self.api_key) and REQUESTS_AVAILABLE

    def get_health(self) -> dict[str, Any]:
        return {
            "provider": self.name,
            "available": self.is_available(),
            "has_api_key": bool(self.api_key),
            "cache_size": len(self._cache),
            "status": "healthy" if self.is_available() else "unavailable",
        }

    def get_available_symbols(self) -> list[str]:
        return ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "XAGUSD"]

    def get_current_quote(self, symbol: str) -> dict[str, Any] | None:
        if not self.is_available():
            return None
        return None  # Alpha Vantage doesn't provide real-time quotes for free

    def get_historical_bars(
        self, symbol: str, timeframe: str, start_date: datetime, end_date: datetime
    ) -> list[OHLCVData]:
        """Get historical data from Alpha Vantage"""
        if not self.is_available():
            return []

        try:
            # Map timeframe to Alpha Vantage function
            func_map = {"D1": "FX_DAILY", "W1": "FX_WEEKLY", "MN1": "FX_MONTHLY"}

            function = func_map.get(timeframe, "FX_DAILY")

            params = {
                "function": function,
                "from_symbol": symbol[:3],
                "to_symbol": symbol[3:6],
                "apikey": self.api_key,
                "outputsize": "full",
            }

            response = requests.get(self.base_url, params=params, timeout=30)

            if response.status_code != 200:
                return []

            data = response.json()

            # Parse the response
            time_series_key = f"Time Series FX ({function.split('_')[1]})"
            if time_series_key not in data:
                return []

            bars = []
            for date_str, values in data[time_series_key].items():
                dt = datetime.strptime(date_str, "%Y-%m-%d")

                # Only include dates within range
                if start_date <= dt <= end_date:
                    bars.append(
                        OHLCVData(
                            symbol=symbol,
                            timeframe=timeframe,
                            timestamp=dt,
                            open=float(values["1. open"]),
                            high=float(values["2. high"]),
                            low=float(values["3. low"]),
                            close=float(values["4. close"]),
                            source=self.name,
                            quality_score=95.0,
                        )
                    )

            return bars

        except Exception as e:
            print(f"Alpha Vantage error for {symbol}: {e}")
            return []
