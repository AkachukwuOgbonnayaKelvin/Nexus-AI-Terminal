from datetime import datetime
from typing import Any, Dict


class NewsValidator:
    def validate(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Validate required fields."""
        required = ["headline", "published_at"]
        for field in required:
            if not record.get(field):
                raise ValueError(f"Missing required field: {field}")
        # Validate timestamp
        if isinstance(record["published_at"], str):
            try:
                datetime.fromisoformat(record["published_at"].replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("Invalid published_at format")
        return record
