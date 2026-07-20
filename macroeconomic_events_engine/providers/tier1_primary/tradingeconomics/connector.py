import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests

from providers.interfaces.base_provider import BaseProvider


class TradingEconomicsConnector(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TRADING_ECONOMICS_API_KEY")
        self.base_url = "https://api.tradingeconomics.com"
        self._connected = bool(self.api_key)
        self._tier = 1
        self._priority = 100

    def connect(self) -> bool:
        return self._connected

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            url = f"{self.base_url}/calendar/country/US?c={self.api_key}&format=json&limit=1"
            resp = requests.get(url, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def get_capabilities(self) -> Dict[str, bool]:
        return {"macroeconomic_events": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_minute": 60}

    def get_available_symbols(self) -> List[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_calendar(
        self, country: str = None, start_date: str = None, end_date: str = None
    ) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
        url = f"{self.base_url}/calendar"
        if country:
            url += f"/country/{country}"
        params = {"c": self.api_key, "format": "json"}
        if start_date:
            params["start"] = start_date
        if end_date:
            params["end"] = end_date
        try:
            resp = requests.get(url, params=params, timeout=10)
            return resp.json() if resp.status_code == 200 else []
        except Exception:
            return []

    def get_today_events(self) -> List[Dict[str, Any]]:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_calendar(start_date=today, end_date=today)

    def get_upcoming_events(self, days: int = 7) -> List[Dict[str, Any]]:
        today = datetime.now().strftime("%Y-%m-%d")
        end = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        return self.get_calendar(start_date=today, end_date=end)
