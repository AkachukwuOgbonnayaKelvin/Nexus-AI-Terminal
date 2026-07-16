#!/usr/bin/env python3
"""Generate central bank provider files for the remaining 7 banks."""


from pathlib import Path

# Project root
ROOT = Path(__file__).parent.parent
PROVIDER_BASE = ROOT / "central_bank_engine" / "providers" / "tier1_primary"

# Bank configurations
BANKS = [
    {
        "name": "ecb",
        "display": "European Central Bank",
        "country": "EU",
        "currency": "EUR",
        "fred_series": None,
        "rss_url": "https://www.ecb.europa.eu/rss/",
        "governor": "Christine Lagarde",
        "priority": 90,
    },
    {
        "name": "boe",
        "display": "Bank of England",
        "country": "UK",
        "currency": "GBP",
        "fred_series": "BOERATE",
        "rss_url": "https://www.bankofengland.co.uk/rss",
        "governor": "Andrew Bailey",
        "priority": 85,
    },
    {
        "name": "boj",
        "display": "Bank of Japan",
        "country": "JP",
        "currency": "JPY",
        "fred_series": "BOJ",
        "rss_url": "https://www.boj.or.jp/en/rss/",
        "governor": "Kazuo Ueda",
        "priority": 85,
    },
    {
        "name": "snb",
        "display": "Swiss National Bank",
        "country": "CH",
        "currency": "CHF",
        "fred_series": "SNB",
        "rss_url": "https://www.snb.ch/en/rss",
        "governor": "Thomas Jordan",
        "priority": 80,
    },
    {
        "name": "boc",
        "display": "Bank of Canada",
        "country": "CA",
        "currency": "CAD",
        "fred_series": "BOC",
        "rss_url": "https://www.bankofcanada.ca/rss/",
        "governor": "Tiff Macklem",
        "priority": 80,
    },
    {
        "name": "rba",
        "display": "Reserve Bank of Australia",
        "country": "AU",
        "currency": "AUD",
        "fred_series": "RBA",
        "rss_url": "https://www.rba.gov.au/rss/",
        "governor": "Michele Bullock",
        "priority": 75,
    },
    {
        "name": "rbnz",
        "display": "Reserve Bank of New Zealand",
        "country": "NZ",
        "currency": "NZD",
        "fred_series": "RBNZ",
        "rss_url": "https://www.rbnz.govt.nz/rss/",
        "governor": "Adrian Orr",
        "priority": 75,
    },
]


def create_provider_files(bank):
    """Generate __init__.py, connector.py, adapter.py for a bank."""
    name = bank["name"]
    display = bank["display"]
    country = bank["country"]
    currency = bank["currency"]
    fred_series = bank.get("fred_series", f"{name.upper()}")
    rss_url = bank["rss_url"]
    governor = bank["governor"]
    priority = bank["priority"]

    bank_dir = PROVIDER_BASE / name
    bank_dir.mkdir(parents=True, exist_ok=True)

    # __init__.py
    init_content = f'''"""Provider for {display} ({name.upper()})."""

from .connector import {name.upper()}Connector
from .adapter import {name.upper()}Adapter

__all__ = ["{name.upper()}Connector", "{name.upper()}Adapter"]
'''
    (bank_dir / "__init__.py").write_text(init_content)

    # connector.py
    connector_content = f'''import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from providers.interfaces.base_provider import BaseProvider

class {name.upper()}Connector(BaseProvider):
    """Connector for {display}."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        self.fred_url = "https://api.stlouisfed.org/fred"
        self.rss_url = "{rss_url}"
        self._connected = bool(self.api_key)
        self._tier = 1
        self._priority = {priority}

    def connect(self) -> bool:
        return self._connected

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        if not self.api_key:
            return False
        try:
            url = f"{{self.fred_url}}/series/observations?series_id={fred_series}&api_key={{self.api_key}}&limit=1"
            resp = requests.get(url, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    def get_capabilities(self) -> Dict[str, bool]:
        return {{"central_bank": True}}

    def get_rate_limit(self) -> Dict[str, int]:
        return {{"requests_per_second": 10, "requests_per_minute": 600}}

    def get_available_symbols(self) -> List[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_policy_rate(self) -> Optional[Dict[str, Any]]:
        """Get the latest policy rate from FRED."""
        if not self.api_key:
            return None
        url = f"{{self.fred_url}}/series/observations?series_id={fred_series}&api_key={{self.api_key}}&limit=1&sort_order=desc"
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if data.get("observations"):
                obs = data["observations"][0]
                return {{
                    "bank": "{display}",
                    "country": "{country}",
                    "currency": "{currency}",
                    "rate": float(obs["value"]),
                    "effective_date": obs["date"],
                    "event_type": "RateDecision",
                    "event_id": f"{name}_rate_latest",
                }}
            return None
        except Exception:
            return None

    def get_today_events(self) -> List[Dict[str, Any]]:
        """Fetch today's events from RSS."""
        # For now, return a stub. In production, parse RSS.
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            {{
                "event_id": f"{name}_schedule_{{today}}",
                "bank": "{display}",
                "country": "{country}",
                "currency": "{currency}",
                "event_type": "MeetingCalendar",
                "title": "{display} Meeting Schedule",
                "release_time": f"{{today}}T14:00:00",
                "communication_type": "Statement",
                "importance": "High",
                "governor": "{governor}",
            }}
        ]
'''
    (bank_dir / "connector.py").write_text(connector_content)

    # adapter.py
    adapter_content = f"""from typing import Dict, Any
from datetime import datetime
from central_bank_engine.dtos import UniversalCentralBankEvent

class {name.upper()}Adapter:
    def adapt(self, raw: Dict[str, Any], provider_name: str) -> UniversalCentralBankEvent:
        release_time = raw.get("release_time") or raw.get("effective_date") or datetime.now().isoformat()
        if isinstance(release_time, str):
            release_time = datetime.fromisoformat(release_time.replace("Z", "+00:00"))

        rate = raw.get("rate")
        old_rate = raw.get("old_rate")
        rate_change = None
        if rate and old_rate:
            rate_change = rate - old_rate

        return UniversalCentralBankEvent(
            event_id=raw.get("event_id", f"{name}_" + release_time.isoformat()),
            provider=provider_name,
            bank=raw.get("bank", "{display}"),
            country=raw.get("country", "{country}"),
            currency=raw.get("currency", "{currency}"),
            event_type=raw.get("event_type", "RateDecision"),
            title=raw.get("title", "{display} Rate Decision"),
            summary=raw.get("summary", ""),
            statement=raw.get("statement", ""),
            release_time=release_time,
            meeting_date=raw.get("meeting_date"),
            effective_date=raw.get("effective_date"),
            old_rate=old_rate,
            new_rate=rate,
            rate_change=rate_change,
            vote_split=raw.get("vote_split"),
            governor=raw.get("governor", "{governor}"),
            importance=raw.get("importance", "High"),
            policy_bias=raw.get("policy_bias"),
            communication_type=raw.get("communication_type", "Statement"),
            source_url=raw.get("source_url"),
            attachments=raw.get("attachments", []),
            confidence=0.95,
            metadata=raw.get("metadata", {{}})
        )
"""
    (bank_dir / "adapter.py").write_text(adapter_content)

    print(f"✅ Created provider for {display}")


def main():
    """Generate all provider files."""
    print("Adding remaining 7 central bank providers...")
    for bank in BANKS:
        create_provider_files(bank)
    print("\n✅ All 7 providers created successfully.")
    print("Next steps:")
    print("1. Run 'python scripts/test_central_bank.py' to verify.")
    print("2. Update the test script to register all providers.")
    print("3. Add real RSS parsing and API endpoints.")


if __name__ == "__main__":
    main()
