"""Base Parser for all COT report types."""

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Abstract base class for all COT parsers."""

    @abstractmethod
    def parse(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Parse COT data into standardized records."""

    @abstractmethod
    def get_report_type(self) -> str:
        """Return the report type this parser handles."""

    def _safe_int(self, value: Any) -> int | None:
        """Safely convert a value to int."""
        if value is None:
            return None
        try:
            if isinstance(value, str):
                cleaned = value.replace(",", "").replace('"', "").strip()
                if cleaned == "" or cleaned == ".":
                    return None
                return int(float(cleaned))
            if isinstance(value, (int, float)):
                return int(value)
            return None
        except (ValueError, TypeError):
            return None

    def _safe_float(self, value: Any) -> float | None:
        """Safely convert a value to float."""
        if value is None:
            return None
        try:
            if isinstance(value, str):
                cleaned = value.replace(",", "").replace('"', "").strip()
                if cleaned == "" or cleaned == ".":
                    return None
                return float(cleaned)
            if isinstance(value, (int, float)):
                return float(value)
            return None
        except (ValueError, TypeError):
            return None

    def _extract_field(self, row: dict[str, Any], *keys: str) -> Any | None:
        """Extract a field from a row using multiple possible keys."""
        for key in keys:
            if key in row and row[key] is not None:
                return row[key]
        return None
