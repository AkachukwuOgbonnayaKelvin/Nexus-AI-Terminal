"""Abstract base class for all adapters."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from providers.dtos.transport import UniversalTransport


class BaseAdapter(ABC):
    """Converts raw provider data to UniversalTransport."""

    @abstractmethod
    def adapt(self, raw_data: Dict[str, Any], source: str) -> UniversalTransport:
        """Convert a single raw record."""
        pass

    @abstractmethod
    def adapt_batch(self, raw_data: List[Dict[str, Any]], source: str) -> List[UniversalTransport]:
        """Convert a batch of raw records."""
        pass
