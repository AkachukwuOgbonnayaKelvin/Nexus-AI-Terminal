"""COT Normalizer – normalizes COT data."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class COTNormalizer:
    def normalize(self, record: dict[str, Any]) -> dict[str, Any]:
        """Normalize a COT record."""
        # Ensure all fields are present with defaults
        normalized = {
            "report_id": record.get("report_id"),
            "report_date": record.get("report_date"),
            "market_code": record.get("market_code"),
            "market_name": record.get("market_name"),
            "asset_class": record.get("asset_class", "unknown"),
            "currency": record.get("currency", "USD"),
            "exchange": record.get("exchange", "CME"),
            "open_interest": record.get("open_interest", 0),
            "dealer_long": record.get("dealer_long"),
            "dealer_short": record.get("dealer_short"),
            "commercial_long": record.get("commercial_long"),
            "commercial_short": record.get("commercial_short"),
            "asset_manager_long": record.get("asset_manager_long"),
            "asset_manager_short": record.get("asset_manager_short"),
            "leveraged_long": record.get("leveraged_long"),
            "leveraged_short": record.get("leveraged_short"),
            "nonreportable_long": record.get("nonreportable_long"),
            "nonreportable_short": record.get("nonreportable_short"),
        }
        return normalized
