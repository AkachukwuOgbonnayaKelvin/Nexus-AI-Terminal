"""Yahoo Finance adapter – converts raw data to UniversalTransport."""

from datetime import datetime
from typing import Any, Dict, List

from providers.dtos.transport import UniversalTransport
from providers.interfaces.base_adapter import BaseAdapter


class YahooAdapter(BaseAdapter):
    """Converts Yahoo raw data to UniversalTransport."""

    def adapt(self, raw_data: Dict[str, Any], source: str) -> UniversalTransport:
        if not raw_data:
            return None

        symbol = raw_data.get("symbol", "unknown")
        timestamp = raw_data.get("timestamp")
        if isinstance(timestamp, str):
            if timestamp.endswith("Z"):
                timestamp = timestamp[:-1] + "+00:00"
            timestamp = datetime.fromisoformat(timestamp)
        else:
            timestamp = datetime.now()

        return UniversalTransport(
            asset=symbol,
            value=raw_data.get("close", 0.0),
            timestamp=timestamp,
            open=raw_data.get("open"),
            high=raw_data.get("high"),
            low=raw_data.get("low"),
            close=raw_data.get("close"),
            volume=raw_data.get("volume"),
            source=source,
            provider="yahoo",
            symbol_provider=symbol,
            asset_class=self._classify(symbol),
            raw_data=raw_data,
            metadata={},
        )

    def adapt_batch(
        self, raw_data: List[Dict[str, Any]], source: str
    ) -> List[UniversalTransport]:
        return [self.adapt(item, source) for item in raw_data if item]

    def _classify(self, symbol: str) -> str:
        if len(symbol) == 6 and symbol.isalpha():
            return "forex"
        elif "-" in symbol:
            return "crypto"
        elif symbol.endswith("=F") or symbol.endswith(".F"):
            return "future"
        else:
            return "equity"
