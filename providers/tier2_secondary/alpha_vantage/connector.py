import os
from datetime import datetime
from typing import Any

import requests

from providers.interfaces.base_provider import BaseProvider


class AlphaVantageConnector(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY", "")
        self._connected = False
        self._tier = 2
        self._priority = 4
        self.base_url = "https://www.alphavantage.co/query"

    def connect(self) -> bool:
        self._connected = bool(self.api_key)
        return self._connected

    def disconnect(self) -> None:
        self._connected = False

    def get_price(self, symbol: str) -> dict[str, Any] | None:
        if not self._connected:
            return None
        if len(symbol) == 6 and symbol.isalpha():
            from_currency = symbol[:3]
            to_currency = symbol[3:]
            params = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_currency,
                "to_currency": to_currency,
                "apikey": self.api_key,
            }
        else:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key,
            }
        try:
            resp = requests.get(self.base_url, params=params, timeout=10)
            data = resp.json()
            if "Realtime Currency Exchange Rate" in data:
                rate = data["Realtime Currency Exchange Rate"]
                return {
                    "symbol": symbol,
                    "price": float(rate["5. Exchange Rate"]),
                    "timestamp": datetime.now().isoformat(),
                    "source": "alpha_vantage",
                    "raw": data,
                }
            elif "Global Quote" in data:
                quote = data["Global Quote"]
                return {
                    "symbol": symbol,
                    "price": float(quote["05. price"]),
                    "timestamp": datetime.now().isoformat(),
                    "source": "alpha_vantage",
                    "raw": data,
                }
            return None
        except Exception:
            return None

    def get_multiple(self, symbols: list[str]) -> list[dict[str, Any]]:
        return [self.get_price(s) for s in symbols if self.get_price(s)]

    def health_check(self) -> bool:
        return self.get_price("EURUSD") is not None

    def get_capabilities(self) -> dict[str, bool]:
        return {"realtime": False, "historical": True, "forex": True, "equities": True}

    def get_rate_limit(self) -> dict[str, int]:
        return {"requests_per_minute": 5}

    def get_available_symbols(self) -> list[str]:
        return ["EURUSD", "AAPL", "MSFT"]

    def supports_symbol(self, symbol: str) -> bool:
        return True
