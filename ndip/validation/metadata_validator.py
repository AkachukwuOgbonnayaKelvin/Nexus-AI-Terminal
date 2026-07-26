"""Metadata Validator – checks required fields and raises on failure."""

from typing import Any


class MetadataValidator:
    def validate(self, record: dict[str, Any]) -> dict[str, Any]:
        """Validate required fields. Returns the record if valid, else raises ValueError."""
        required = ["symbol", "asset_class"]
        for field in required:
            if not record.get(field):
                raise ValueError(f"Missing required field: {field}")
        return record
