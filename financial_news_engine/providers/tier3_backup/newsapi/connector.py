import os
from typing import Any, Dict, List, Optional

import requests

from providers.interfaces.base_provider import BaseProvider


class NewsAPIConnector(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NEWSAPI_API_KEY")
        self.base_url = "https://newsapi.org/v2"
        self._connected = bool(self.api_key)
        self._tier = 3
        self._priority = 10

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
            url = f"{self.base_url}/top-headlines?country=us&apiKey={self.api_key}"
            resp = requests.get(url, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def get_capabilities(self) -> Dict[str, bool]:
        return {"news": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_day": 100}

    def get_available_symbols(self) -> List[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_top_headlines(
        self, country: str = "us", category: str = None, page_size: int = 20
    ) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
        url = f"{self.base_url}/top-headlines"
        params = {"country": country, "apiKey": self.api_key, "pageSize": page_size}
        if category:
            params["category"] = category
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get("status") == "ok":
                return data.get("articles", [])
            return []
        except Exception:
            return []

    def get_everything(self, query: str, page_size: int = 20) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
        url = f"{self.base_url}/everything"
        params = {"q": query, "apiKey": self.api_key, "pageSize": page_size}
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get("status") == "ok":
                return data.get("articles", [])
            return []
        except Exception:
            return []

    def get_today_news(self) -> List[Dict[str, Any]]:
        # Get top headlines from US for a broad coverage
        return self.get_top_headlines(country="us", page_size=20)
