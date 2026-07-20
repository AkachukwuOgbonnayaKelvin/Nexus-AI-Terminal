import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import feedparser

from providers.interfaces.base_provider import BaseProvider


class ECBConnector(BaseProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        self.rss_url = "https://www.ecb.europa.eu/rss/"
        self._connected = True
        self._tier = 1
        self._priority = 90

    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        return True

    def get_capabilities(self) -> Dict[str, bool]:
        return {"central_bank": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_second": 10, "requests_per_minute": 600}

    def get_available_symbols(self) -> List[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_policy_rate(self) -> Optional[Dict[str, Any]]:
        # ECB rate stub – will be replaced with ECB SDW API later
        return {
            "bank": "European Central Bank",
            "country": "EU",
            "currency": "EUR",
            "rate": 3.00,
            "effective_date": datetime.now().strftime("%Y-%m-%d"),
            "event_type": "RateDecision",
            "event_id": "ecb_rate_latest",
        }

    def get_today_events(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries[:10]:
                title = entry.title.lower()
                if "interest" in title or "rate" in title:
                    event_type = "RateDecision"
                elif "minutes" in title:
                    event_type = "Minutes"
                elif "speech" in title or "press" in title:
                    event_type = "Speech"
                else:
                    event_type = "Statement"
                published = entry.published_parsed
                release_time = datetime(*published[:6]) if published else datetime.now()
                events.append(
                    {
                        "event_id": f"ecb_{entry.id.split('/')[-1]}"
                        if "/" in entry.id
                        else f"ecb_{release_time.isoformat()}",
                        "bank": "European Central Bank",
                        "country": "EU",
                        "currency": "EUR",
                        "event_type": event_type,
                        "title": entry.title,
                        "summary": entry.summary,
                        "release_time": release_time.isoformat(),
                        "source_url": entry.link,
                        "governor": "Christine Lagarde",
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
                    "event_id": f"ecb_schedule_{today}",
                    "bank": "European Central Bank",
                    "country": "EU",
                    "currency": "EUR",
                    "event_type": "MeetingCalendar",
                    "title": "ECB Meeting Schedule",
                    "release_time": f"{today}T14:00:00",
                    "communication_type": "Statement",
                    "importance": "High",
                    "governor": "Christine Lagarde",
                }
            )
        return events
