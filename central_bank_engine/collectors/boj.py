"""Bank of Japan collectors (Rate, Speech, Minutes, Statement, Calendar)."""

import os
from datetime import datetime
from typing import Any

import feedparser
import requests

from central_bank_engine.collectors.base import (
    CalendarCollector,
    MinutesCollector,
    RateCollector,
    SpeechCollector,
    StatementCollector,
)


class BOJRateCollector(RateCollector):
    """Collects Bank of Japan interest rates."""

    def __init__(self, bank_id: str = "boj"):
        super().__init__(bank_id)
        self.api_key = os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.series_id = "BOJ"
        self.rate_placeholder = 0.5

    async def collect(self) -> list[dict[str, Any]]:
        events = []
        if self.api_key and self.series_id:
            url = f"{self.fred_url}/series/observations?series_id={self.series_id}&api_key={self.api_key}&limit=1&sort_order=desc"
            try:
                resp = requests.get(url, timeout=10)
                data = resp.json()
                if data.get("observations"):
                    obs = data["observations"][0]
                    events.append(
                        {
                            "event_id": f"boj_rate_{obs['date']}",
                            "bank": "Bank of Japan",
                            "country": "JP",
                            "currency": "JPY",
                            "event_type": "RATE_DECISION",
                            "title": "Bank of Japan Interest Rate",
                            "rate": float(obs["value"]),
                            "effective_date": obs["date"],
                            "source": "FRED",
                            "confidence": 1.0,
                        }
                    )
            except Exception:
                pass
        if not events:
            events.append(
                {
                    "event_id": f"boj_rate_{datetime.now().date()}",
                    "bank": "Bank of Japan",
                    "country": "JP",
                    "currency": "JPY",
                    "event_type": "RATE_DECISION",
                    "title": "Bank of Japan Interest Rate",
                    "rate": 0.5,
                    "effective_date": datetime.now().date().isoformat(),
                    "source": "placeholder",
                    "confidence": 0.5,
                }
            )
        return events


class BOJSpeechCollector(SpeechCollector):
    """Collects Bank of Japan speeches from RSS."""

    def __init__(self, bank_id: str = "boj"):
        super().__init__(bank_id)
        self.rss_url = "https://www.boj.or.jp/en/rss/"

    async def collect(self) -> list[dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "speech" in title or "testimony" in title:
                    published = entry.published_parsed
                    release_time = (
                        datetime(*published[:6]) if published else datetime.now()
                    )
                    events.append(
                        {
                            "event_id": f"boj_speech_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"boj_speech_{release_time.isoformat()}",
                            "bank": "Bank of Japan",
                            "country": "JP",
                            "currency": "JPY",
                            "event_type": "SPEECH",
                            "title": entry.title,
                            "summary": entry.summary,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "governor": "Kazuo Ueda",
                            "source": "RSS",
                        }
                    )
        except Exception:
            pass
        return events


class BOJMinutesCollector(MinutesCollector):
    """Collects Bank of Japan meeting minutes from RSS."""

    def __init__(self, bank_id: str = "boj"):
        super().__init__(bank_id)
        self.rss_url = "https://www.boj.or.jp/en/rss/"

    async def collect(self) -> list[dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "minutes" in title:
                    published = entry.published_parsed
                    release_time = (
                        datetime(*published[:6]) if published else datetime.now()
                    )
                    events.append(
                        {
                            "event_id": f"boj_minutes_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"boj_minutes_{release_time.isoformat()}",
                            "bank": "Bank of Japan",
                            "country": "JP",
                            "currency": "JPY",
                            "event_type": "MINUTES",
                            "title": entry.title,
                            "summary": entry.summary,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "source": "RSS",
                        }
                    )
        except Exception:
            pass
        return events


class BOJStatementCollector(StatementCollector):
    """Collects Bank of Japan policy statements from RSS."""

    def __init__(self, bank_id: str = "boj"):
        super().__init__(bank_id)
        self.rss_url = "https://www.boj.or.jp/en/rss/"

    async def collect(self) -> list[dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "statement" in title or "announcement" in title or "press" in title:
                    if "minutes" not in title and "speech" not in title:
                        published = entry.published_parsed
                        release_time = (
                            datetime(*published[:6]) if published else datetime.now()
                        )
                        events.append(
                            {
                                "event_id": f"boj_statement_{entry.id.split('/')[-1]}"
                                if "/" in entry.id
                                else f"boj_statement_{release_time.isoformat()}",
                                "bank": "Bank of Japan",
                                "country": "JP",
                                "currency": "JPY",
                                "event_type": "STATEMENT",
                                "title": entry.title,
                                "summary": entry.summary,
                                "release_time": release_time.isoformat(),
                                "source_url": entry.link,
                                "source": "RSS",
                            }
                        )
        except Exception:
            pass
        return events


class BOJCalendarCollector(CalendarCollector):
    """Collects Bank of Japan meeting calendar."""

    def __init__(self, bank_id: str = "boj"):
        super().__init__(bank_id)
        self.rss_url = "https://www.boj.or.jp/en/rss/"

    async def collect(self) -> list[dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "schedule" in title or "calendar" in title:
                    published = entry.published_parsed
                    release_time = (
                        datetime(*published[:6]) if published else datetime.now()
                    )
                    events.append(
                        {
                            "event_id": f"boj_calendar_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"boj_calendar_{release_time.isoformat()}",
                            "bank": "Bank of Japan",
                            "country": "JP",
                            "currency": "JPY",
                            "event_type": "MEETING",
                            "title": entry.title,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "source": "RSS",
                        }
                    )
        except Exception:
            pass
        if not events:
            events.append(
                {
                    "event_id": "boj_calendar_placeholder",
                    "bank": "Bank of Japan",
                    "country": "JP",
                    "currency": "JPY",
                    "event_type": "MEETING",
                    "title": "Bank of Japan Meeting Calendar",
                    "release_time": datetime.now().isoformat(),
                    "source": "placeholder",
                }
            )
        return events
