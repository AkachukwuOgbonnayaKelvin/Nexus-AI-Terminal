import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from providers.interfaces.base_provider import BaseProvider


class FederalReserveConnector(BaseProvider):
    """Connector for Federal Reserve (FRED + FOMC)."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        self.base_url = "https://api.stlouisfed.org/fred"
        self._connected = True  # Always connected for mock data
        self._tier = 1
        self._priority = 100

    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        # Always return True for mock data; if API key is present, test it
        if self.api_key:
            try:
                url = f"{self.base_url}/series/observations?series_id=FEDFUNDS&api_key={self.api_key}&limit=1"
                resp = requests.get(url, timeout=5)
                return resp.status_code == 200
            except Exception:
                return False
        return True

    def get_capabilities(self) -> Dict[str, bool]:
        return {"central_bank": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_second": 10, "requests_per_minute": 600}

    def get_available_symbols(self) -> List[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_fed_funds_rate(self) -> Optional[Dict[str, Any]]:
        """Get the latest Federal Funds Rate."""
        if not self.api_key:
            # Return mock rate if no key
            return {
                "bank": "Federal Reserve",
                "country": "US",
                "currency": "USD",
                "rate": 4.75,
                "effective_date": datetime.now().strftime("%Y-%m-%d"),
                "event_type": "RateDecision",
                "event_id": "fed_rate_mock",
                "title": "Federal Funds Rate",
                "release_time": datetime.now().isoformat(),
            }
        try:
            url = (
                f"{self.base_url}/series/observations?series_id=FEDFUNDS&api_key={self.api_key}&limit=1&sort_order=desc"
            )
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data.get("observations"):
                obs = data["observations"][0]
                return {
                    "bank": "Federal Reserve",
                    "country": "US",
                    "currency": "USD",
                    "rate": float(obs["value"]),
                    "effective_date": obs["date"],
                    "event_type": "RateDecision",
                    "event_id": "fed_rate_latest",
                    "title": "Federal Funds Rate",
                    "release_time": f"{obs['date']}T00:00:00",
                }
            return None
        except Exception:
            return None

    def get_today_events(self) -> List[Dict[str, Any]]:
        """Fetch today's events (mock for now)."""
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            {
                "event_id": f"fed_schedule_{today}",
                "bank": "Federal Reserve",
                "country": "US",
                "currency": "USD",
                "event_type": "MeetingCalendar",
                "title": "FOMC Meeting Schedule",
                "release_time": f"{today}T14:00:00",
                "communication_type": "Statement",
                "importance": "High",
                "summary": "Next FOMC meeting scheduled",
                "metadata": {"source": "mock"},
            }
        ]
