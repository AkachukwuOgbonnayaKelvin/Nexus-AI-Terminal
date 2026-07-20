from abc import abstractmethod
from datetime import date
from typing import Any, Dict, List, Optional

from providers.interfaces.base_provider import BaseProvider


class BaseEconomicProvider(BaseProvider):
    @abstractmethod
    def get_today_events(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_event(self, series_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_historical_series(
        self, series_id: str, start: date, end: date
    ) -> List[Dict[str, Any]]:
        pass
