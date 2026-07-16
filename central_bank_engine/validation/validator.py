from datetime import datetime
from typing import Any, Dict


class CentralBankValidator:
    def validate(self, record: Dict[str, Any]) -> Dict[str, Any]:
        required = [
            "event_id",
            "bank",
            "country",
            "currency",
            "event_type",
            "release_time",
        ]
        for field in required:
            if not record.get(field):
                raise ValueError(f"Missing required field: {field}")
        if isinstance(record["release_time"], str):
            try:
                datetime.fromisoformat(record["release_time"].replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("Invalid release_time format")
        return record
