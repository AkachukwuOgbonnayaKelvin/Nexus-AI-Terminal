"""Abstract base class for all adapters."""

from abc import ABC, abstractmethod
from typing import Any

from providers.dtos.transport import UniversalTransport


class BaseAdapter(ABC):
    """Converts raw provider data to UniversalTransport."""

    @abstractmethod
    def adapt(self, raw_data: dict[str, Any], source: str) -> UniversalTransport:
        """Convert a single raw record."""

    @abstractmethod
    def adapt_batch(
        self, raw_data: list[dict[str, Any]], source: str
    ) -> list[UniversalTransport]:
        """Convert a batch of raw records."""
