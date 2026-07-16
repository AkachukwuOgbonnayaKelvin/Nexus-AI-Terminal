"""Swiss National Bank collectors (Rate, Speech, Minutes, Statement, Calendar)."""

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


class SNBRateCollector(RateCollector):
    """Collects Swiss National Bank interest rates."""

    def __init__(self, bank_id: str = "snb"):
        super().__init__(bank_id)
        self.api_key = os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.series_id = "SNB"
        self.rate_placeholder = 0.75

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
                            "event_id": f"snb_rate_{obs['date']}",
                            "bank": "Swiss National Bank",
                            "country": "CH",
                            "currency": "CHF",
                            "event_type": "RATE_DECISION",
                            "title": "Swiss National Bank Interest Rate",
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
                    "event_id": f"snb_rate_{datetime.now().date()}",
                    "bank": "Swiss National Bank",
                    "country": "CH",
                    "currency": "CHF",
                    "event_type": "RATE_DECISION",
                    "title": "Swiss National Bank Interest Rate",
                    "rate": 0.75,
                    "effective_date": datetime.now().date().isoformat(),
                    "source": "placeholder",
                    "confidence": 0.5,
                }
            )
        return events


class SNBSpeechCollector(SpeechCollector):
    """Collects Swiss National Bank speeches from RSS."""

    def __init__(self, bank_id: str = "snb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.snb.ch/en/rss"

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
                            "event_id": f"snb_speech_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"snb_speech_{release_time.isoformat()}",
                            "bank": "Swiss National Bank",
                            "country": "CH",
                            "currency": "CHF",
                            "event_type": "SPEECH",
                            "title": entry.title,
                            "summary": entry.summary,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "governor": "Thomas Jordan",
                            "source": "RSS",
                        }
                    )
        except Exception:
            pass
        return events


class SNBMinutesCollector(MinutesCollector):
    """Collects Swiss National Bank meeting minutes from RSS."""

    def __init__(self, bank_id: str = "snb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.snb.ch/en/rss"

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
                            "event_id": f"snb_minutes_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"snb_minutes_{release_time.isoformat()}",
                            "bank": "Swiss National Bank",
                            "country": "CH",
                            "currency": "CHF",
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


class SNBStatementCollector(StatementCollector):
    """Collects Swiss National Bank policy statements from RSS."""

    def __init__(self, bank_id: str = "snb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.snb.ch/en/rss"

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
                                "event_id": f"snb_statement_{entry.id.split('/')[-1]}"
                                if "/" in entry.id
                                else f"snb_statement_{release_time.isoformat()}",
                                "bank": "Swiss National Bank",
                                "country": "CH",
                                "currency": "CHF",
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


class SNBCalendarCollector(CalendarCollector):
    """Collects Swiss National Bank meeting calendar."""

    def __init__(self, bank_id: str = "snb"):
        super().__init__(bank_id)
        self.rss_url = "https://www.snb.ch/en/rss"

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
                            "event_id": f"snb_calendar_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"snb_calendar_{release_time.isoformat()}",
                            "bank": "Swiss National Bank",
                            "country": "CH",
                            "currency": "CHF",
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
                    "event_id": "snb_calendar_placeholder",
                    "bank": "Swiss National Bank",
                    "country": "CH",
                    "currency": "CHF",
                    "event_type": "MEETING",
                    "title": "Swiss National Bank Meeting Calendar",
                    "release_time": datetime.now().isoformat(),
                    "source": "placeholder",
                }
            )
        return events
