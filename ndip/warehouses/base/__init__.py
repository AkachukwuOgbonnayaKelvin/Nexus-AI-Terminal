"""Abstract base class for all NDIP warehouses."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class BaseWarehouse(ABC):
    """Base class for domain-specific warehouses."""

    def __init__(self, name: str):
        self.name = name
        self._table_name = None  # To be set by subclass

    @abstractmethod
    async def store(self, record: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Store a single record in the warehouse."""
        pass

    @abstractmethod
    async def query(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Query records by symbol."""
        pass

    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Return warehouse statistics."""
        pass

    async def health_check(self) -> bool:
        """Check if warehouse is operational."""
        try:
            await self.get_stats()
            return True
        except Exception:
            return False
