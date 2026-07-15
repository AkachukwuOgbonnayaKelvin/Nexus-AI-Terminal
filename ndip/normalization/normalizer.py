"""NDIP Normalizer implementation."""

from typing import Any, Dict


class Normalizer:
    """Data normalizer."""

    def __init__(self):
        self._standard_fields = {
            "timestamp": "timestamp",
            "asset": "symbol",
            "value": "price",
            "volume": "volume",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
        }

    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize data to standard format."""
        if "records" in data:
            return {"records": [self._normalize_record(r) for r in data["records"]]}

        return {"record": self._normalize_record(data.get("record", {}))}

    def _normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a single record."""
        normalized = {}

        # Map fields to standard names
        for field, value in record.items():
            standard_name = self._standard_fields.get(field, field)
            normalized[standard_name] = value

        return normalized
