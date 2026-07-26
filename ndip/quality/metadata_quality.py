"""Metadata Quality Controller – scores and assesses metadata quality."""

from typing import Any


class MetadataQualityController:
    def score(self, record: dict[str, Any], provider: str) -> float:
        """Calculate quality score based on completeness and provider."""
        score = 1.0
        # Reduce score for missing fields
        important_fields = ["symbol", "asset_class", "exchange_code", "currency"]
        for field in important_fields:
            if not record.get(field):
                score -= 0.2
        # Provider quality adjustment
        if provider.startswith("mt5"):
            score *= 1.1
        elif provider.startswith("yahoo"):
            score *= 0.9
        return max(0.0, min(1.0, score))
