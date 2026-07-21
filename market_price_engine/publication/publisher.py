# -*- coding: utf-8 -*-
"""MKT-001 NDIP Publisher"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class MarketPricePublisher:
    """Publisher for market price data"""

    def __init__(self):
        self._published = []
        self.topics = ["market.price.ohlcv", "market.price.tick"]

    def publish(self, data: Dict[str, Any]) -> bool:
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

    def publish_many(self, records: List[Dict[str, Any]]) -> int:
        """Publish multiple records"""
        count = 0
        for record in records:
            if self.publish(record):
                count += 1
        return count

    def exists(self, record_id: str) -> bool:
        """Check if a record exists in NDIP"""
        return any(r.get("record_id") == record_id for r in self._published)

    def get_latest(self) -> Optional[Dict[str, Any]]:
        """Get the latest published record"""
        if not self._published:
            return None
        return max(self._published, key=lambda x: x.get("timestamp", ""))

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all published records"""
        return self._published.copy()

    def get_count(self) -> int:
        """Get total published count"""
        return len(self._published)

    def get_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID"""
        for record in self._published:
            if record.get("record_id") == record_id:
                return record
        return None

    def _get_topic(self, data: Dict[str, Any]) -> str:
        """Determine the topic based on data content"""
        if "timeframe" in data or "ohlcv" in str(data).lower():
            return "market.price.ohlcv"
        if "bid" in data or "ask" in data:
            return "market.price.tick"
        return "market.price.data"
