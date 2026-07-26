"""Knowledge Linker – maps events to affected assets."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class KnowledgeLinker:
    ASSET_MAP = {
        "Federal Reserve": ["USD", "Gold", "US10Y", "US500", "US30"],
        "European Central Bank": ["EUR", "EURUSD", "Bund", "GER40"],
        "Bank of England": ["GBP", "GBPUSD", "Gilt", "UK100"],
        "Bank of Japan": ["JPY", "USDJPY", "JGB", "JP225"],
        "Swiss National Bank": ["CHF", "USDCHF", "Gold"],
        "Bank of Canada": ["CAD", "USDCAD", "Oil"],
        "Reserve Bank of Australia": ["AUD", "AUDUSD", "Gold"],
        "Reserve Bank of New Zealand": ["NZD", "NZDUSD", "Dairy"],
    }

    def link(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for event in events:
            bank = event.get("bank")
            assets = self.ASSET_MAP.get(bank, [])
            event["affected_assets"] = assets
            event["knowledge_graph"] = {
                "bank": bank,
                "currency": event.get("currency"),
                "assets": assets,
            }
        logger.info(f"Linked {len(events)} events to assets")
        return events
