"""Base interface for all raw data engines."""

from abc import ABC, abstractmethod
from typing import Any


class BaseRawEngine(ABC):
    @abstractmethod
    async def initialize(self) -> None:
        pass

    @abstractmethod
    async def run(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass

    @abstractmethod
    def health(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def metrics(self) -> dict[str, Any]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def enabled(self) -> bool:
        pass

    @property
    @abstractmethod
    def interval_seconds(self) -> int:
        pass
