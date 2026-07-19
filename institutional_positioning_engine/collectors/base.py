"""Base class for COT collectors."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseCollector(ABC):
    def __init__(self, provider_manager):
        self.provider_manager = provider_manager

    @abstractmethod
    async def collect_all(self) -> List[Dict[str, Any]]:
        """Collect all historical reports."""
        pass

    @abstractmethod
    async def collect_latest(self) -> List[Dict[str, Any]]:
        """Collect the latest report."""
        pass
