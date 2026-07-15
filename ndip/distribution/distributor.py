"""NDIP Distributor implementation."""

from typing import Any, Dict, List


class Distributor:
    """Data distributor."""

    def __init__(self):
        self._consumers: Dict[str, Any] = {}
        self._subscriptions: Dict[str, List[str]] = {}

    def register_consumer(self, name: str, consumer: Any) -> None:
        """Register a data consumer."""
        self._consumers[name] = consumer

    def subscribe(self, consumer: str, symbol: str) -> None:
        """Subscribe a consumer to a symbol."""
        if consumer not in self._subscriptions:
            self._subscriptions[consumer] = []
        self._subscriptions[consumer].append(symbol)

    def distribute(self, symbol: str, data: Any) -> Dict[str, Any]:
        """Distribute data to consumers."""
        distributed = 0
        errors = []

        for consumer_name, symbols in self._subscriptions.items():
            if symbol in symbols:
                try:
                    consumer = self._consumers.get(consumer_name)
                    if consumer:
                        consumer.receive(symbol, data)
                        distributed += 1
                except Exception as e:
                    errors.append({"consumer": consumer_name, "error": str(e)})

        return {
            "symbol": symbol,
            "distributed_to": distributed,
            "errors": errors,
        }
