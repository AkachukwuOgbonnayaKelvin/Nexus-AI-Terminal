"""NDIP Classifier implementation."""

from typing import Any, Dict


class Classifier:
    """Data classifier."""

    def __init__(self) -> None:
        self._asset_classes: Dict[str, list[str]] = {
            "forex": ["USD", "EUR", "JPY", "GBP", "CHF", "CAD", "AUD", "NZD"],
            "commodity": ["XAU", "XAG", "WTI", "BRENT", "NG", "COPPER"],
            "index": ["US30", "US500", "US100", "GER40", "UK100"],
        }

    def classify(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify data by type."""
        if "records" in data:
            return {"records": [self._classify_record(r) for r in data["records"]]}

        return {"record": self._classify_record(data.get("record", {}))}

    def _classify_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Classify a single record."""
        symbol = record.get("symbol", "")

        # Determine asset class
        asset_class = "unknown"
        for class_type, symbols in self._asset_classes.items():
            if symbol in symbols:
                asset_class = class_type
                break

        record["asset_class"] = asset_class
        return record
