from datetime import datetime
from typing import Any, Dict, List

from providers.dtos.transport import UniversalTransport
from providers.interfaces.base_adapter import BaseAdapter


class MT5Adapter(BaseAdapter):
    def adapt(self, raw_data: Dict[str, Any], source: str) -> UniversalTransport:
        if not raw_data:
            return None
        symbol = raw_data.get("symbol", "unknown")
        timestamp = raw_data.get("time")
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp)
        return UniversalTransport(
            asset=symbol,
            value=raw_data.get("ask", raw_data.get("last", 0.0)),
            timestamp=timestamp or datetime.now(),
            volume=raw_data.get("volume"),
            source=source,
            provider="mt5",
            symbol_provider=symbol,
            asset_class=self._classify(symbol),
            raw_data=raw_data,
            metadata={
                "bid": raw_data.get("bid"),
                "ask": raw_data.get("ask"),
                "spread": raw_data.get("spread"),
            },
        )

    def adapt_batch(self, raw_data: List[Dict[str, Any]], source: str) -> List[UniversalTransport]:
        return [self.adapt(item, source) for item in raw_data if item]

    def _classify(self, symbol: str) -> str:
        if symbol.isalpha() and len(symbol) <= 6:
            return "forex"
        elif "BTC" in symbol or "ETH" in symbol:
            return "crypto"
        elif symbol.startswith("XAU") or symbol.startswith("XAG"):
            return "commodity"
        else:
            return "cfd"
