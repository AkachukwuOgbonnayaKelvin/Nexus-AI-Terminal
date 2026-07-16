"""Knowledge Linking – connects central bank events to other platform data."""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class KnowledgeLinker:
    def __init__(self):
        self.bank_currency_map = {
            "Federal Reserve": "USD",
            "ECB": "EUR",
            "Bank of England": "GBP",
            "Bank of Japan": "JPY",
            "Swiss National Bank": "CHF",
            "Bank of Canada": "CAD",
            "Reserve Bank of Australia": "AUD",
            "Reserve Bank of New Zealand": "NZD",
        }
        self.asset_links = {
            "Federal Reserve": ["USD", "Gold", "US10Y", "US500", "US30"],
            "ECB": ["EUR", "EURUSD", "Bund", "GER40"],
            "Bank of England": ["GBP", "GBPUSD", "Gilt", "UK100"],
            "Bank of Japan": ["JPY", "USDJPY", "JGB", "JP225"],
        }

    def link(self, event: Dict[str, Any]) -> Dict[str, Any]:
        bank = event.get("bank", "")
        currency = self.bank_currency_map.get(bank, "USD")
        assets = self.asset_links.get(bank, [currency])
        event["linked_currency"] = currency
        event["linked_assets"] = assets
        return event
