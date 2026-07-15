"""NDIP Warehouse implementation."""

from typing import Any, Dict, List
from collections import defaultdict


class Warehouse:
    """Data warehouse."""

    def __init__(self) -> None:
        self._data: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._indices: Dict[str, Dict[str, int]] = defaultdict(dict)

    def store(self, data: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Store data in the warehouse."""
        if "records" in data:
            stored_count = 0
            for record in data["records"]:
                self._store_record(record, source)
                stored_count += 1
            return {"stored": stored_count, "source": source}

        if "record" in data:
            self._store_record(data["record"], source)
            return {"stored": 1, "source": source}

        return {"stored": 0, "source": source}

    def _store_record(self, record: Dict[str, Any], source: str) -> None:
        """Store a single record."""
        symbol = record.get("symbol", "unknown")
        self._data[symbol].append(record)

        # Update index
        if symbol not in self._indices:
            self._indices[symbol] = {}
        self._indices[symbol][source] = len(self._data[symbol]) - 1

    def query(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Query data by symbol."""
        records = self._data.get(symbol, [])
        return records[-limit:] if limit > 0 else records

    def get_stats(self) -> Dict[str, Any]:
        """Get warehouse statistics."""
        return {
            "total_symbols": len(self._data),
            "total_records": sum(len(v) for v in self._data.values()),
            "symbols": list(self._data.keys()),
        }
