"""Base classes for central bank collectors."""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """Abstract base class for all collectors."""

    def __init__(self, bank_id: str):
        self.bank_id = bank_id
        self.name = self.__class__.__name__
        self.last_run: datetime | None = None
        self.success_count = 0
        self.error_count = 0
        self.is_running = False

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        """Collect data and return a list of raw events."""

    def log_success(self):
        self.success_count += 1
        self.last_run = datetime.now()
        logger.info(f"{self.name} for {self.bank_id} succeeded")

    def log_error(self, error: Exception):
        self.error_count += 1
        logger.error(f"{self.name} for {self.bank_id} error: {error}")

    def get_status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "bank_id": self.bank_id,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "is_running": self.is_running,
        }


class RateCollector(BaseCollector):
    """Collect interest rate decisions."""

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        pass


class SpeechCollector(BaseCollector):
    """Collect governor speeches."""

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        pass


class MinutesCollector(BaseCollector):
    """Collect meeting minutes."""

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        pass


class StatementCollector(BaseCollector):
    """Collect monetary policy statements."""

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        pass


class CalendarCollector(BaseCollector):
    """Collect meeting calendars."""

    @abstractmethod
    async def collect(self) -> list[dict[str, Any]]:
        pass
