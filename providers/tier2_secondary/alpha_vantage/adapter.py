from datetime import datetime
from typing import Any, Dict, List

from providers.dtos.transport import UniversalTransport
from providers.interfaces.base_adapter import BaseAdapter


class AlphaVantageAdapter(BaseAdapter):
    def adapt(self, raw_data: Dict[str, Any], source: str) -> UniversalTransport:
        if not raw_data:
            return None
        symbol = raw_data.get("symbol", "unknown")
        price = raw_data.get("price", 0.0)
        timestamp = raw_data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        return UniversalTransport(
            asset=symbol,
            value=price,
            timestamp=timestamp or datetime.now(),
            source=source,
            provider="alpha_vantage",
            symbol_provider=symbol,
            asset_class="forex"
            if (len(symbol) == 6 and symbol.isalpha())
            else "equity",
            raw_data=raw_data,
        )

    def adapt_batch(
        self, raw_data: List[Dict[str, Any]], source: str
    ) -> List[UniversalTransport]:
        return [self.adapt(item, source) for item in raw_data if item]
