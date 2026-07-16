import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from providers.interfaces.base_provider import BaseProvider


class PolygonConnector(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("POLYGON_API_KEY", "")
        self._connected = False
        self._tier = 1
        self._priority = 80

    def connect(self) -> bool:
        self._connected = bool(self.api_key)
        return self._connected

    def disconnect(self) -> None:
        self._connected = False

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        if not self._connected:
            return None
        url = f"https://api.polygon.io/v1/last/stocks/{symbol}?apiKey={self.api_key}"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            if data.get("status") == "OK":
                last = data.get("last")
                return {
                    "symbol": symbol,
                    "price": last.get("price"),
                    "volume": last.get("volume"),
                    "timestamp": datetime.now().isoformat(),
                    "source": "polygon",
                    "raw": data,
                }
            return None
        except Exception:
            return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return [self.get_price(s) for s in symbols if self.get_price(s)]

    def health_check(self) -> bool:
        return self.get_price("AAPL") is not None

    def get_capabilities(self) -> Dict[str, bool]:
        return {"realtime": True, "historical": True, "equities": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_minute": 60}

    def get_available_symbols(self) -> List[str]:
        return ["AAPL", "MSFT", "GOOGL"]

    def supports_symbol(self, symbol: str) -> bool:
        return True
