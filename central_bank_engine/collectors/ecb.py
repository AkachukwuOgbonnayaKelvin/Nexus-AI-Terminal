"""European Central Bank collectors (Rate, Speech, Minutes, Statement, Calendar)."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import feedparser
import requests

from central_bank_engine.collectors.base import (
    CalendarCollector,
    MinutesCollector,
    RateCollector,
    SpeechCollector,
    StatementCollector,
)


class ECBRateCollector(RateCollector):
    """Collects European Central Bank interest rates."""

    def __init__(self, bank_id: str = "ecb"):
        super().__init__(bank_id)
        self.api_key = os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.series_id = "None"
        self.rate_placeholder = 3.0

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
                            "event_id": f"ecb_rate_{obs['date']}",
                            "bank": "European Central Bank",
                            "country": "EU",
                            "currency": "EUR",
                            "event_type": "RATE_DECISION",
                            "title": "European Central Bank Interest Rate",
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
                    "event_id": f"ecb_rate_{datetime.now().date()}",
                    "bank": "European Central Bank",
                    "country": "EU",
                    "currency": "EUR",
                    "event_type": "RATE_DECISION",
                    "title": "European Central Bank Interest Rate",
                    "rate": 3.0,
                    "effective_date": datetime.now().date().isoformat(),
                    "source": "placeholder",
                    "confidence": 0.5,
                }
            )
        return events


class ECBSpeechCollector(SpeechCollector):
    """Collects European Central Bank speeches from RSS."""

    def __init__(self, bank_id: str = "ecb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.ecb.europa.eu/rss/"

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
                            "event_id": f"ecb_speech_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"ecb_speech_{release_time.isoformat()}",
                            "bank": "European Central Bank",
                            "country": "EU",
                            "currency": "EUR",
                            "event_type": "SPEECH",
                            "title": entry.title,
                            "summary": entry.summary,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "governor": "Christine Lagarde",
                            "source": "RSS",
                        }
                    )
        except Exception:
            pass
        return events


class ECBMinutesCollector(MinutesCollector):
    """Collects European Central Bank meeting minutes from RSS."""

    def __init__(self, bank_id: str = "ecb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.ecb.europa.eu/rss/"

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
                            "event_id": f"ecb_minutes_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"ecb_minutes_{release_time.isoformat()}",
                            "bank": "European Central Bank",
                            "country": "EU",
                            "currency": "EUR",
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


class ECBStatementCollector(StatementCollector):
    """Collects European Central Bank policy statements from RSS."""

    def __init__(self, bank_id: str = "ecb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.ecb.europa.eu/rss/"

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
                                "event_id": f"ecb_statement_{entry.id.split('/')[-1]}"
                                if "/" in entry.id
                                else f"ecb_statement_{release_time.isoformat()}",
                                "bank": "European Central Bank",
                                "country": "EU",
                                "currency": "EUR",
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


class ECBCalendarCollector(CalendarCollector):
    """Collects European Central Bank meeting calendar."""

    def __init__(self, bank_id: str = "ecb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.ecb.europa.eu/rss/"

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
                            "event_id": f"ecb_calendar_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"ecb_calendar_{release_time.isoformat()}",
                            "bank": "European Central Bank",
                            "country": "EU",
                            "currency": "EUR",
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
                    "event_id": f"ecb_calendar_placeholder",
                    "bank": "European Central Bank",
                    "country": "EU",
                    "currency": "EUR",
                    "event_type": "MEETING",
                    "title": "European Central Bank Meeting Calendar",
                    "release_time": datetime.now().isoformat(),
                    "source": "placeholder",
                }
            )
        return events
