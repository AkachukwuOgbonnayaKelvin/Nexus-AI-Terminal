from datetime import datetime
from typing import Any

from providers.interfaces.base_provider import BaseProvider


class ForexFactoryConnector(BaseProvider):
    def __init__(self):
        self._connected = True
        self._tier = 2
        self._priority = 60

    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> dict[str, Any] | None:
        return None

    def get_multiple(self, symbols: list[str]) -> list[dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        return True

    def get_capabilities(self) -> dict[str, bool]:
        return {"macroeconomic_events": True}

    def get_rate_limit(self) -> dict[str, int]:
        return {"requests_per_minute": 10}

    def get_available_symbols(self) -> list[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_today_events(self) -> list[dict[str, Any]]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            {
                "event_id": f"ff_us_cpi_{today}",
                "provider": "forexfactory",
                "country": "US",
                "currency": "USD",
                "title": "Consumer Price Index",
                "category": "Inflation",
                "forecast": 2.8,
                "previous": 2.6,
                "release_time_utc": f"{today}T08:30:00",
                "importance": "High",
                "actual": None,
                "status": "Scheduled",
            },
            {
                "event_id": f"ff_ecb_rate_{today}",
                "provider": "forexfactory",
                "country": "EU",
                "currency": "EUR",
                "title": "ECB Interest Rate Decision",
                "category": "Central Bank",
                "forecast": 3.0,
                "previous": 3.25,
                "release_time_utc": f"{today}T12:45:00",
                "importance": "High",
                "actual": None,
                "status": "Scheduled",
            },
            {
                "event_id": f"ff_us_jobless_{today}",
                "provider": "forexfactory",
                "country": "US",
                "currency": "USD",
                "title": "Initial Jobless Claims",
                "category": "Labour",
                "forecast": 220,
                "previous": 215,
                "release_time_utc": f"{today}T13:30:00",
                "importance": "Medium",
                "actual": None,
                "status": "Scheduled",
            },
        ]
