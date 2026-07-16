#!/usr/bin/env python3
"""Generate collector files for all central banks."""


from pathlib import Path

ROOT = Path(__file__).parent.parent
COLLECTOR_DIR = ROOT / "central_bank_engine" / "collectors"

BANKS = [
    {
        "id": "ecb",
        "name": "European Central Bank",
        "currency": "EUR",
        "country": "EU",
        "rss_url": "https://www.ecb.europa.eu/rss/",
        "governor": "Christine Lagarde",
        "rate_series": None,
        "rate_placeholder": 3.0,
    },
    {
        "id": "boe",
        "name": "Bank of England",
        "currency": "GBP",
        "country": "UK",
        "rss_url": "https://www.bankofengland.co.uk/rss",
        "governor": "Andrew Bailey",
        "rate_series": "BOERATE",
        "rate_placeholder": 3.75,
    },
    {
        "id": "boj",
        "name": "Bank of Japan",
        "currency": "JPY",
        "country": "JP",
        "rss_url": "https://www.boj.or.jp/en/rss/",
        "governor": "Kazuo Ueda",
        "rate_series": "BOJ",
        "rate_placeholder": 0.50,
    },
    {
        "id": "snb",
        "name": "Swiss National Bank",
        "currency": "CHF",
        "country": "CH",
        "rss_url": "https://www.snb.ch/en/rss",
        "governor": "Thomas Jordan",
        "rate_series": "SNB",
        "rate_placeholder": 0.75,
    },
    {
        "id": "boc",
        "name": "Bank of Canada",
        "currency": "CAD",
        "country": "CA",
        "rss_url": "https://www.bankofcanada.ca/rss/",
        "governor": "Tiff Macklem",
        "rate_series": "BOC",
        "rate_placeholder": 4.00,
    },
    {
        "id": "rba",
        "name": "Reserve Bank of Australia",
        "currency": "AUD",
        "country": "AU",
        "rss_url": "https://www.rba.gov.au/rss/",
        "governor": "Michele Bullock",
        "rate_series": "RBA",
        "rate_placeholder": 3.25,
    },
    {
        "id": "rbnz",
        "name": "Reserve Bank of New Zealand",
        "currency": "NZD",
        "country": "NZ",
        "rss_url": "https://www.rbnz.govt.nz/rss/",
        "governor": "Adrian Orr",
        "rate_series": "RBNZ",
        "rate_placeholder": 2.75,
    },
]

TEMPLATE_RATE = '''"""{} collectors (Rate, Speech, Minutes, Statement, Calendar)."""

import os
import feedparser
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from central_bank_engine.collectors.base import (
    RateCollector,
    SpeechCollector,
    MinutesCollector,
    StatementCollector,
    CalendarCollector,
)

class {}RateCollector(RateCollector):
    """Collects {} interest rates."""

    def __init__(self, bank_id: str = "{}"):
        super().__init__(bank_id)
        self.api_key = os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.series_id = "{}"
        self.rate_placeholder = {}

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        if self.api_key and self.series_id:
            url = f"{{self.fred_url}}/series/observations?series_id={{self.series_id}}&api_key={{self.api_key}}&limit=1&sort_order=desc"
            try:
                resp = requests.get(url, timeout=10)
                data = resp.json()
                if data.get("observations"):
                    obs = data["observations"][0]
                    events.append({{
                        "event_id": f"{}_rate_{{obs['date']}}",
                        "bank": "{}",
                        "country": "{}",
                        "currency": "{}",
                        "event_type": "RATE_DECISION",
                        "title": "{} Interest Rate",
                        "rate": float(obs["value"]),
                        "effective_date": obs["date"],
                        "source": "FRED",
                        "confidence": 1.0,
                    }})
            except Exception:
                pass
        if not events:
            events.append({{
                "event_id": f"{}_rate_{{datetime.now().date()}}",
                "bank": "{}",
                "country": "{}",
                "currency": "{}",
                "event_type": "RATE_DECISION",
                "title": "{} Interest Rate",
                "rate": {},
                "effective_date": datetime.now().date().isoformat(),
                "source": "placeholder",
                "confidence": 0.5,
            }})
        return events

class {}SpeechCollector(SpeechCollector):
    """Collects {} speeches from RSS."""

    def __init__(self, bank_id: str = "{}"):
        super().__init__(bank_id)
        self.rss_url = "{}"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "speech" in title or "testimony" in title:
                    published = entry.published_parsed
                    release_time = datetime(*published[:6]) if published else datetime.now()
                    events.append({{
                        "event_id": f"{}_speech_{{entry.id.split('/')[-1]}}" if '/' in entry.id else f"{}_speech_{{release_time.isoformat()}}",
                        "bank": "{}",
                        "country": "{}",
                        "currency": "{}",
                        "event_type": "SPEECH",
                        "title": entry.title,
                        "summary": entry.summary,
                        "release_time": release_time.isoformat(),
                        "source_url": entry.link,
                        "governor": "{}",
                        "source": "RSS",
                    }})
        except Exception:
            pass
        return events

class {}MinutesCollector(MinutesCollector):
    """Collects {} meeting minutes from RSS."""

    def __init__(self, bank_id: str = "{}"):
        super().__init__(bank_id)
        self.rss_url = "{}"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "minutes" in title:
                    published = entry.published_parsed
                    release_time = datetime(*published[:6]) if published else datetime.now()
                    events.append({{
                        "event_id": f"{}_minutes_{{entry.id.split('/')[-1]}}" if '/' in entry.id else f"{}_minutes_{{release_time.isoformat()}}",
                        "bank": "{}",
                        "country": "{}",
                        "currency": "{}",
                        "event_type": "MINUTES",
                        "title": entry.title,
                        "summary": entry.summary,
                        "release_time": release_time.isoformat(),
                        "source_url": entry.link,
                        "source": "RSS",
                    }})
        except Exception:
            pass
        return events

class {}StatementCollector(StatementCollector):
    """Collects {} policy statements from RSS."""

    def __init__(self, bank_id: str = "{}"):
        super().__init__(bank_id)
        self.rss_url = "{}"

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
                        events.append({{
                            "event_id": f"{}_statement_{{entry.id.split('/')[-1]}}" if '/' in entry.id else f"{}_statement_{{release_time.isoformat()}}",
                            "bank": "{}",
                            "country": "{}",
                            "currency": "{}",
                            "event_type": "STATEMENT",
                            "title": entry.title,
                            "summary": entry.summary,
                            "release_time": release_time.isoformat(),
                            "source_url": entry.link,
                            "source": "RSS",
                        }})
        except Exception:
            pass
        return events

class {}CalendarCollector(CalendarCollector):
    """Collects {} meeting calendar."""

    def __init__(self, bank_id: str = "{}"):
        super().__init__(bank_id)
        self.rss_url = "{}"

    async def collect(self) -> List[Dict[str, Any]]:
        events = []
        try:
            feed = feedparser.parse(self.rss_url)
            for entry in feed.entries:
                title = entry.title.lower()
                if "schedule" in title or "calendar" in title:
                    published = entry.published_parsed
                    release_time = datetime(*published[:6]) if published else datetime.now()
                    events.append({{
                        "event_id": f"{}_calendar_{{entry.id.split('/')[-1]}}" if '/' in entry.id else f"{}_calendar_{{release_time.isoformat()}}",
                        "bank": "{}",
                        "country": "{}",
                        "currency": "{}",
                        "event_type": "MEETING",
                        "title": entry.title,
                        "release_time": release_time.isoformat(),
                        "source_url": entry.link,
                        "source": "RSS",
                    }})
        except Exception:
            pass
        if not events:
            events.append({{
                "event_id": f"{}_calendar_placeholder",
                "bank": "{}",
                "country": "{}",
                "currency": "{}",
                "event_type": "MEETING",
                "title": "{} Meeting Calendar",
                "release_time": datetime.now().isoformat(),
                "source": "placeholder",
            }})
        return events
'''


def generate_collectors(bank):
    bank_id = bank["id"]
    name = bank["name"]
    currency = bank["currency"]
    country = bank["country"]
    rss_url = bank["rss_url"]
    governor = bank["governor"]
    rate_series = bank.get("rate_series", "NONE")
    rate_placeholder = bank.get("rate_placeholder", 2.0)

    class_name = bank_id.upper()
    content = TEMPLATE_RATE.format(
        name,  # doc string
        class_name,  # RateCollector class name
        name,  # doc
        bank_id,  # bank_id
        rate_series,  # series_id
        rate_placeholder,  # placeholder
        bank_id,  # event_id prefix
        name,  # bank name
        country,  # country
        currency,  # currency
        name,  # title
        bank_id,  # event_id prefix (fallback)
        name,  # bank name
        country,
        currency,
        name,
        rate_placeholder,
        class_name,  # SpeechCollector class name
        name,  # doc
        bank_id,  # bank_id
        rss_url,  # rss_url
        bank_id,  # event_id prefix
        bank_id,
        name,
        country,
        currency,
        governor,
        class_name,  # MinutesCollector
        name,
        bank_id,
        rss_url,
        bank_id,
        bank_id,
        name,
        country,
        currency,
        class_name,  # StatementCollector
        name,
        bank_id,
        rss_url,
        bank_id,
        bank_id,
        name,
        country,
        currency,
        class_name,  # CalendarCollector
        name,
        bank_id,
        rss_url,
        bank_id,
        bank_id,
        name,
        country,
        currency,
        bank_id,
        name,
        country,
        currency,
        name,
    )
    file_path = COLLECTOR_DIR / f"{bank_id}.py"
    file_path.write_text(content)
    print(f"✅ Generated {bank_id}.py")


def main():
    COLLECTOR_DIR.mkdir(parents=True, exist_ok=True)
    for bank in BANKS:
        generate_collectors(bank)
    print("\nAll collector files generated.")


if __name__ == "__main__":
    main()
