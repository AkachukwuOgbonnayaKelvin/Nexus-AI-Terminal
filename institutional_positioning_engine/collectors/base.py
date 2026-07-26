"""Base class for COT collectors."""

from abc import ABC, abstractmethod
from typing import Any


class BaseCollector(ABC):
    def __init__(self, provider_manager):
        self.provider_manager = provider_manager

    @abstractmethod
    async def collect_all(self) -> list[dict[str, Any]]:
        """Collect all historical reports."""

    @abstractmethod
    async def collect_latest(self) -> list[dict[str, Any]]:
        """Collect the latest report."""
