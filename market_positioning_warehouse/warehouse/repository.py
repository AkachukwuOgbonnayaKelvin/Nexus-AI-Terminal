"""Repository – Data access layer for the warehouse."""

import logging
from typing import List

from market_positioning_warehouse.dtos import UniversalPosition

logger = logging.getLogger(__name__)


class Repository:
    """Repository for position data."""

    def __init__(self):
        self._storage: List[UniversalPosition] = []
        self._counter = 0

    async def store(self, position: UniversalPosition) -> bool:
        """Store a position record."""
        try:
            self._storage.append(position)
            self._counter += 1
            logger.debug(
                f"Stored position: {position.market_name} - {position.report_date}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store position: {e}")
            return False

    async def get_unprocessed(self, limit: int = 1000) -> List[UniversalPosition]:
        """Get unprocessed positions."""
        # Return all positions for now
        return self._storage[:limit]

    async def get_count(self) -> int:
        """Get total record count."""
        return self._counter

    async def get_by_market(self, market_name: str) -> List[UniversalPosition]:
        """Get positions for a specific market."""
        return [p for p in self._storage if p.market_name == market_name]

    async def get_by_date(self, date: str) -> List[UniversalPosition]:
        """Get positions for a specific date."""
        return [p for p in self._storage if str(p.report_date) == date]

    async def clear(self) -> None:
        """Clear all stored data (for testing)."""
        self._storage.clear()
        self._counter = 0
