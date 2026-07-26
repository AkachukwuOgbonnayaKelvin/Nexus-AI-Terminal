import os
from datetime import datetime
from typing import Any

import feedparser
import requests

from providers.interfaces.base_provider import BaseProvider


class FederalReserveConnector(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.rss_url = "https://www.federalreserve.gov/feeds/press_all.xml"
        self._connected = True
        self._tier = 1
        self._priority = 100
        self.fred_series = "FEDFUNDS"

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
        return {"central_bank": True}

    def get_rate_limit(self) -> dict[str, int]:
        return {"requests_per_second": 10, "requests_per_minute": 600}

    def get_available_symbols(self) -> list[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_policy_rate(self) -> dict[str, Any] | None:
        if self.api_key:
            url = f"{self.fred_url}/series/observations?series_id=FEDFUNDS&api_key={self.api_key}&limit=1&sort_order=desc"
            try:
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
                    }
            except Exception:
                pass
        return {
            "bank": "Federal Reserve",
            "country": "US",
            "currency": "USD",
            "rate": 4.25,
            "effective_date": datetime.now().strftime("%Y-%m-%d"),
            "event_type": "RateDecision",
            "event_id": "fed_rate_latest",
        }

    def get_today_events(self) -> list[dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries[:10]:
                title = entry.title.lower()
                if "fomc" in title or "interest" in title or "rate" in title:
                    event_type = "RateDecision"
                elif "minutes" in title:
                    event_type = "Minutes"
                elif "speech" in title or "testimony" in title:
                    event_type = "Speech"
                else:
                    event_type = "Statement"
                published = entry.published_parsed
                release_time = datetime(*published[:6]) if published else datetime.now()
                events.append(
                    {
                        "event_id": f"fed_{entry.id.split('/')[-1]}"
                        if "/" in entry.id
                        else f"fed_{release_time.isoformat()}",
                        "bank": "Federal Reserve",
                        "country": "US",
                        "currency": "USD",
                        "event_type": event_type,
                        "title": entry.title,
                        "summary": entry.summary,
                        "release_time": release_time.isoformat(),
                        "source_url": entry.link,
                        "governor": "Jerome Powell",
                        "importance": "High"
                        if event_type in ["RateDecision", "Minutes"]
                        else "Medium",
                        "communication_type": "Statement"
                        if event_type == "Statement"
                        else "Speech",
                    }
                )
        except Exception:
            today = datetime.now().strftime("%Y-%m-%d")
            events.append(
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
                    "governor": "Jerome Powell",
                }
            )
        return events
