"""Metadata Normalizer – standardizes field names and formats."""

from typing import Any, Dict


class MetadataNormalizer:
    def normalize(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize field names and values."""
        # Example: ensure certain fields are present with defaults
        record.setdefault("display_symbol", record.get("symbol"))
        record.setdefault("short_name", "")
        record.setdefault("long_name", "")
        return record
