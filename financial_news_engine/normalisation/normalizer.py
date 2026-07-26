from typing import Any


class NewsNormalizer:
    def normalize(self, record: dict[str, Any]) -> dict[str, Any]:
        """Normalize field names and values."""
        # Ensure article_id is present
        if "article_id" not in record:
            record["article_id"] = (
                f"news_{record.get('provider', 'unknown')}_{record.get('published_at', '')}"
            )
        # Ensure language is set
        if "language" not in record:
            record["language"] = "en"
        # Truncate body if too long
        if "body" in record and record["body"] and len(record["body"]) > 10000:
            record["body"] = record["body"][:10000] + "..."
        return record
