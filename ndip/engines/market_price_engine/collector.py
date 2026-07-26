"""Market Price Collector with real data from Yahoo Finance."""

import time
from datetime import datetime
from typing import Any

from ndip.gateway import DataGateway


class MarketPriceCollector:
    """Collects real market price data from Yahoo Finance."""

    def __init__(self, gateway: DataGateway) -> None:
        self.gateway = gateway
        self._connectors: dict[str, Any] = {}
        self._running: bool = False
        self._last_collection: datetime | None = None

    def register_connector(self, name: str, connector: Any) -> None:
        """Register a data connector."""
        self._connectors[name] = connector
        self.gateway.register_source(name, connector)

    def collect(self, symbol: str, source: str = "yahoo") -> dict[str, Any]:
        """Collect real price data for a symbol."""
        if source not in self._connectors:
            raise ValueError(f"Unknown source: {source}")

        connector = self._connectors[source]
        if not hasattr(connector, "get_price"):
            raise ValueError(f"Connector {source} does not support get_price")

        # Fetch real data
        data = connector.get_price(symbol)

        if data is None:
            return {
                "symbol": symbol,
                "error": "No data received from source",
                "source": source,
                "timestamp": datetime.now().isoformat(),
            }

        # Add source and timestamp if not present
        data["source"] = source
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()

        # Send to NDIP pipeline
        result = self.gateway.ingest(source, data)
        return result

    def collect_batch(
        self, symbols: list[str], source: str = "yahoo"
    ) -> list[dict[str, Any]]:
        """Collect real price data for multiple symbols."""
        results = []
        for symbol in symbols:
            result = self.collect(symbol, source)
            results.append(result)
            time.sleep(0.5)  # Rate limiting
        return results

    def start(self) -> None:
        """Start the collector."""
        self._running = True
        self._last_collection = datetime.now()

        # Connect all registered connectors
        for _name, connector in self._connectors.items():
            if hasattr(connector, "connect"):
                connector.connect()

    def stop(self) -> None:
        """Stop the collector."""
        self._running = False

        # Disconnect all registered connectors
        for _name, connector in self._connectors.items():
            if hasattr(connector, "disconnect"):
                connector.disconnect()

    def get_stats(self) -> dict[str, Any]:
        """Get collector statistics."""
        return {
            "running": self._running,
            "connectors": list(self._connectors.keys()),
            "last_collection": self._last_collection,
            "total_connectors": len(self._connectors),
        }
