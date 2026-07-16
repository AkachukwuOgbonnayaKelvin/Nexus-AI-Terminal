from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from providers.interfaces.base_provider import BaseProvider


class BinanceConnector(BaseProvider):
    def __init__(self):
        self._connected = True
        self._tier = 3
        self._priority = 3
        self.base_url = "https://api.binance.com/api/v3"

    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        binance_symbol = symbol.replace("-", "").upper()
        url = f"{self.base_url}/ticker/price?symbol={binance_symbol}"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            if "price" in data:
                return {
                    "symbol": binance_symbol,
                    "price": float(data["price"]),
                    "timestamp": datetime.now().isoformat(),
                    "source": "binance",
                    "raw": data,
                }
            return None
        except Exception:
            return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return [self.get_price(s) for s in symbols if self.get_price(s)]

    def health_check(self) -> bool:
        return self.get_price("BTCUSDT") is not None

    def get_capabilities(self) -> Dict[str, bool]:
        return {"realtime": True, "historical": True, "crypto": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_minute": 1200}

    def get_available_symbols(self) -> List[str]:
        return ["BTCUSDT", "ETHUSDT"]

    def supports_symbol(self, symbol: str) -> bool:
        return True
