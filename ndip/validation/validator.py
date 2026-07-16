"""NDIP Validator implementation."""

from datetime import datetime
from typing import Any, Dict


class Validator:
    """Data validator."""

    def __init__(self) -> None:
        self._required_fields: list[str] = ["timestamp", "asset", "value"]

    def validate(self, data: Any) -> Dict[str, Any]:
        """Validate incoming data."""
        if isinstance(data, list):
            return {"records": [self._validate_record(r) for r in data]}

        return {"record": self._validate_record(data)}

    def _validate_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single record."""
        # Check required fields
        for field in self._required_fields:
            if field not in record:
                raise ValueError(f"Missing required field: {field}")

        # Validate timestamp
        try:
            datetime.fromisoformat(record["timestamp"])
        except (ValueError, TypeError):
            raise ValueError("Invalid timestamp format")

        # Validate value is numeric
        if not isinstance(record.get("value"), (int, float)):
            raise ValueError("Value must be numeric")

        return record
