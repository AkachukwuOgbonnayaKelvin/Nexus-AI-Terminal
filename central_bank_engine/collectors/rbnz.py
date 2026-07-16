"""Reserve Bank of New Zealand collectors (Rate, Speech, Minutes, Statement, Calendar)."""

import os
from datetime import datetime
from typing import Any, Dict, List

import feedparser
import requests

from central_bank_engine.collectors.base import (
    CalendarCollector,
    MinutesCollector,
    RateCollector,
    SpeechCollector,
    StatementCollector,
)


class RBNZRateCollector(RateCollector):
    """Collects Reserve Bank of New Zealand interest rates."""

    def __init__(self, bank_id: str = "rbnz"):
        super().__init__(bank_id)
        self.api_key = os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.series_id = "RBNZ"
        self.rate_placeholder = 2.75

    async def collect(self) -> List[Dict[str, Any]]:
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
                            "event_id": f"rbnz_rate_{obs['date']}",
                            "bank": "Reserve Bank of New Zealand",
                            "country": "NZ",
                            "currency": "NZD",
                            "event_type": "RATE_DECISION",
                            "title": "Reserve Bank of New Zealand Interest Rate",
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
                    "event_id": f"rbnz_rate_{datetime.now().date()}",
                    "bank": "Reserve Bank of New Zealand",
                    "country": "NZ",
                    "currency": "NZD",
                    "event_type": "RATE_DECISION",
                    "title": "Reserve Bank of New Zealand Interest Rate",
                    "rate": 2.75,
                    "effective_date": datetime.now().date().isoformat(),
                    "source": "placeholder",
                    "confidence": 0.5,
                }
            )
        return events


class RBNZSpeechCollector(SpeechCollector):
    """Collects Reserve Bank of New Zealand speeches from RSS."""

    def __init__(self, bank_id: str = "rbnz"):
        super().__init__(bank_id)
        self.rss_url = "https://www.rbnz.govt.nz/rss/"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "speech" in title or "testimony" in title:
                    published = entry.published_parsed
                    release_time = datetime(*published[:6]) if published else datetime.now()
                    events.append(
                        {
                            "event_id": f"rbnz_speech_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"rbnz_speech_{release_time.isoformat()}",
                            "bank": "Reserve Bank of New Zealand",
                            "country": "NZ",
                            "currency": "NZD",
                            "event_type": "SPEECH",
                            "title": entry.title,
                            "summary": entry.summary,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "governor": "Adrian Orr",
                            "source": "RSS",
                        }
                    )
        except Exception:
            pass
        return events


class RBNZMinutesCollector(MinutesCollector):
    """Collects Reserve Bank of New Zealand meeting minutes from RSS."""

    def __init__(self, bank_id: str = "rbnz"):
        super().__init__(bank_id)
        self.rss_url = "https://www.rbnz.govt.nz/rss/"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "minutes" in title:
                    published = entry.published_parsed
                    release_time = datetime(*published[:6]) if published else datetime.now()
                    events.append(
                        {
                            "event_id": f"rbnz_minutes_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"rbnz_minutes_{release_time.isoformat()}",
                            "bank": "Reserve Bank of New Zealand",
                            "country": "NZ",
                            "currency": "NZD",
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


class RBNZStatementCollector(StatementCollector):
    """Collects Reserve Bank of New Zealand policy statements from RSS."""

    def __init__(self, bank_id: str = "rbnz"):
        super().__init__(bank_id)
        self.rss_url = "https://www.rbnz.govt.nz/rss/"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "statement" in title or "announcement" in title or "press" in title:
                    if "minutes" not in title and "speech" not in title:
                        published = entry.published_parsed
                        release_time = datetime(*published[:6]) if published else datetime.now()
                        events.append(
                            {
                                "event_id": f"rbnz_statement_{entry.id.split('/')[-1]}"
                                if "/" in entry.id
                                else f"rbnz_statement_{release_time.isoformat()}",
                                "bank": "Reserve Bank of New Zealand",
                                "country": "NZ",
                                "currency": "NZD",
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


class RBNZCalendarCollector(CalendarCollector):
    """Collects Reserve Bank of New Zealand meeting calendar."""

    def __init__(self, bank_id: str = "rbnz"):
        super().__init__(bank_id)
        self.rss_url = "https://www.rbnz.govt.nz/rss/"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "schedule" in title or "calendar" in title:
                    published = entry.published_parsed
                    release_time = datetime(*published[:6]) if published else datetime.now()
                    events.append(
                        {
                            "event_id": f"rbnz_calendar_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"rbnz_calendar_{release_time.isoformat()}",
                            "bank": "Reserve Bank of New Zealand",
                            "country": "NZ",
                            "currency": "NZD",
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
                    "event_id": "rbnz_calendar_placeholder",
                    "bank": "Reserve Bank of New Zealand",
                    "country": "NZ",
                    "currency": "NZD",
                    "event_type": "MEETING",
                    "title": "Reserve Bank of New Zealand Meeting Calendar",
                    "release_time": datetime.now().isoformat(),
                    "source": "placeholder",
                }
            )
        return events
