"""MKT-001 NDIP Publisher"""

from datetime import datetime
from typing import Any


class MarketPricePublisher:
    """Publisher for market price data"""

    def __init__(self):
        self._published = []
        self.topics = ["market.price.ohlcv", "market.price.tick"]

    def publish(self, data: dict[str, Any]) -> bool:
        """Publish a single record"""
        if not data:
            return False
        record = {
            "topic": self._get_topic(data),
            "data": data,
            "record_id": data.get("record_id", f"record_{len(self._published)}"),
            "timestamp": datetime.now().isoformat(),
            "published_at": datetime.now().isoformat(),
        }
        self._published.append(record)
        return True

    def publish_many(self, records: list[dict[str, Any]]) -> int:
        """Publish multiple records"""
        count = 0
        for record in records:
            if self.publish(record):
                count += 1
        return count

    def exists(self, record_id: str) -> bool:
        """Check if a record exists in NDIP"""
        return any(r.get("record_id") == record_id for r in self._published)

    def get_latest(self) -> dict[str, Any] | None:
        """Get the latest published record"""
        if not self._published:
            return None
        return max(self._published, key=lambda x: x.get("timestamp", ""))

    def get_all(self) -> list[dict[str, Any]]:
        """Get all published records"""
        return self._published.copy()

    def get_count(self) -> int:
        """Get total published count"""
        return len(self._published)

    def get_by_id(self, record_id: str) -> dict[str, Any] | None:
        """Get a record by ID"""
        for record in self._published:
            if record.get("record_id") == record_id:
                return record
        return None

    def _get_topic(self, data: dict[str, Any]) -> str:
        """Determine the topic based on data content"""
        if "timeframe" in data or "ohlcv" in str(data).lower():
            return "market.price.ohlcv"
        if "bid" in data or "ask" in data:
            return "market.price.tick"
        return "market.price.data"
