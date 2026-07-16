from datetime import date
from typing import Any, Dict, List, Optional

import pandas_datareader.data as web

from economic_events_engine.providers.interfaces.base_economic_provider import BaseEconomicProvider


class FredConnector(BaseEconomicProvider):
    def __init__(self):
        self._connected = True
        self._tier = 2
        self._priority = 50

    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        pass

    def get_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None

    def get_multiple(self, symbols: List[str]) -> List[Dict[str, Any]]:
        return []

    def health_check(self) -> bool:
        try:
            data = web.DataReader("GDP", "fred", start="2000-01-01", end="2000-01-02")
            return not data.empty
        except Exception:
            return False

    def get_capabilities(self) -> Dict[str, bool]:
        return {"economic": True}

    def get_rate_limit(self) -> Dict[str, int]:
        return {"requests_per_second": 10, "requests_per_minute": 600}

    def get_available_symbols(self) -> List[str]:
        return []

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def get_today_events(self) -> List[Dict[str, Any]]:
        return []

    def get_event(self, series_id: str) -> Optional[Dict[str, Any]]:
        try:
            data = web.DataReader(series_id, "fred", start="2000-01-01")
            if data.empty:
                return None
            latest = data.iloc[-1]
            return {
                "series_id": series_id,
                "value": float(latest.iloc[0]),
                "date": latest.name.isoformat(),
                "source": "fred",
            }
        except Exception:
            return None

    def get_historical_series(self, series_id: str, start: date, end: date) -> List[Dict[str, Any]]:
        try:
            data = web.DataReader(series_id, "fred", start=start, end=end)
            if data.empty:
                return []
            result = []
            for idx, row in data.iterrows():
                result.append(
                    {
                        "series_id": series_id,
                        "value": float(row.iloc[0]),
                        "date": idx.isoformat(),
                        "source": "fred",
                    }
                )
            return result
        except Exception:
            return []
