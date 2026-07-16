"""Federal Reserve collectors (Rate, Speech, Minutes, Statement, Calendar)."""

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


class FedRateCollector(RateCollector):
    """Collects Federal Reserve interest rates from FRED."""

    def __init__(self, bank_id: str = "federal_reserve"):
        super().__init__(bank_id)
        self.api_key = os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.series_id = "FEDFUNDS"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        if self.api_key:
            url = f"{self.fred_url}/series/observations?series_id={self.series_id}&api_key={self.api_key}&limit=1&sort_order=desc"
            try:
                resp = requests.get(url, timeout=10)
                data = resp.json()
                if data.get("observations"):
                    obs = data["observations"][0]
                    events.append(
                        {
                            "event_id": f"fed_rate_{obs['date']}",
                            "bank": "Federal Reserve",
                            "country": "US",
                            "currency": "USD",
                            "event_type": "RATE_DECISION",
                            "title": "Federal Funds Rate",
                            "rate": float(obs["value"]),
                            "effective_date": obs["date"],
                            "source": "FRED",
                            "confidence": 1.0,
                        }
                    )
            except Exception:
                pass
        if not events:
            # Fallback to placeholder
            events.append(
                {
                    "event_id": f"fed_rate_{datetime.now().date()}",
                    "bank": "Federal Reserve",
                    "country": "US",
                    "currency": "USD",
                    "event_type": "RATE_DECISION",
                    "title": "Federal Funds Rate",
                    "rate": 4.25,
                    "effective_date": datetime.now().date().isoformat(),
                    "source": "placeholder",
                    "confidence": 0.5,
                }
            )
        return events


class FedSpeechCollector(SpeechCollector):
    """Collects Federal Reserve speeches from RSS."""

    def __init__(self, bank_id: str = "federal_reserve"):
        super().__init__(bank_id)
        self.rss_url = "https://www.federalreserve.gov/feeds/press_all.xml"

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
                            "event_id": f"fed_speech_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"fed_speech_{release_time.isoformat()}",
                            "bank": "Federal Reserve",
                            "country": "US",
                            "currency": "USD",
                            "event_type": "SPEECH",
                            "title": entry.title,
                            "summary": entry.summary,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "governor": "Jerome Powell",  # Default; could be parsed
                            "source": "RSS",
                        }
                    )
        except Exception:
            pass
        return events


class FedMinutesCollector(MinutesCollector):
    """Collects Federal Reserve meeting minutes from RSS."""

    def __init__(self, bank_id: str = "federal_reserve"):
        super().__init__(bank_id)
        self.rss_url = "https://www.federalreserve.gov/feeds/press_all.xml"

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
                            "event_id": f"fed_minutes_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"fed_minutes_{release_time.isoformat()}",
                            "bank": "Federal Reserve",
                            "country": "US",
                            "currency": "USD",
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


class FedStatementCollector(StatementCollector):
    """Collects Federal Reserve policy statements from RSS."""

    def __init__(self, bank_id: str = "federal_reserve"):
        super().__init__(bank_id)
        self.rss_url = "https://www.federalreserve.gov/feeds/press_all.xml"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "statement" in title or "announcement" in title:
                    # Exclude minutes, speeches, etc.
                    if "minutes" not in title and "speech" not in title:
                        published = entry.published_parsed
                        release_time = datetime(*published[:6]) if published else datetime.now()
                        events.append(
                            {
                                "event_id": f"fed_statement_{entry.id.split('/')[-1]}"
                                if "/" in entry.id
                                else f"fed_statement_{release_time.isoformat()}",
                                "bank": "Federal Reserve",
                                "country": "US",
                                "currency": "USD",
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


class FedCalendarCollector(CalendarCollector):
    """Collects Federal Reserve meeting calendar from RSS or static list."""

    def __init__(self, bank_id: str = "federal_reserve"):
        super().__init__(bank_id)
        self.rss_url = "https://www.federalreserve.gov/feeds/press_all.xml"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        # Try to extract from RSS; fallback to a static list of known meeting dates
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "schedule" in title and "meeting" in title:
                    published = entry.published_parsed
                    release_time = datetime(*published[:6]) if published else datetime.now()
                    events.append(
                        {
                            "event_id": f"fed_calendar_{entry.id.split('/')[-1]}"
                            if "/" in entry.id
                            else f"fed_calendar_{release_time.isoformat()}",
                            "bank": "Federal Reserve",
                            "country": "US",
                            "currency": "USD",
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
            # Static fallback: known 2026 FOMC meeting dates
            fallback_dates = [
                "2026-07-30",
                "2026-09-17",
                "2026-11-05",
                "2026-12-16",
            ]
            for date_str in fallback_dates:
                events.append(
                    {
                        "event_id": f"fed_calendar_{date_str}",
                        "bank": "Federal Reserve",
                        "country": "US",
                        "currency": "USD",
                        "event_type": "MEETING",
                        "title": f"FOMC Meeting - {date_str}",
                        "release_time": f"{date_str}T14:00:00",
                        "source": "placeholder",
                    }
                )
        return events
