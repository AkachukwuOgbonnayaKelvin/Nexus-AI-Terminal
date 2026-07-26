from abc import abstractmethod
from datetime import date
from typing import Any

from providers.interfaces.base_provider import BaseProvider


class BaseEconomicProvider(BaseProvider):
    @abstractmethod
    def get_today_events(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_event(self, series_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def get_historical_series(
        self, series_id: str, start: date, end: date
    ) -> list[dict[str, Any]]:
        pass
