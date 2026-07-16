"""PriceWarehouse – stores market prices per asset class."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from ndip.utils.db_connector import fetch, fetchrow
from ndip.warehouses.base import BaseWarehouse

logger = logging.getLogger(__name__)


class PriceWarehouse(BaseWarehouse):
    """Warehouse for all price data."""

    TABLE_MAP = {
        "forex": "price_forex",
        "commodity": "price_commodities",
        "index": "price_indices",
        "equity": "price_stocks",
        "crypto": "price_crypto",
    }

    def __init__(self):
        super().__init__("price")

    def _get_table(self, asset_class: str) -> str:
        table = self.TABLE_MAP.get(asset_class)
        if not table:
            raise ValueError(f"Unknown asset class: {asset_class}")
        return table

    async def store(self, record: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Store a price record."""
        asset_class = record.get("asset_class", "unknown")
        table = self._get_table(asset_class)

        # Convert timestamp string to datetime
        time_val = record.get("timestamp")
        if isinstance(time_val, str):
            if time_val.endswith("Z"):
                time_val = time_val[:-1] + "+00:00"
            time_val = datetime.fromisoformat(time_val)
        elif time_val is None:
            time_val = datetime.now()

        symbol = record.get("symbol") or record.get("asset")
        price = record.get("value") or record.get("price")
        volume = record.get("volume")
        open_p = record.get("open")
        high = record.get("high")
        low = record.get("low")
        close = record.get("close")
        metadata = record.get("metadata", {})

        # Convert metadata to JSON string if it's a dict
        if isinstance(metadata, dict):
            metadata = json.dumps(metadata)

        query = f"""
            INSERT INTO {table} (time, symbol, price, volume, open, high, low, close, source, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING time, symbol
        """
        await fetchrow(
            query,
            time_val,
            symbol,
            price,
            volume,
            open_p,
            high,
            low,
            close,
            source,
            metadata,
        )
        return {"stored": True, "table": table, "symbol": symbol, "time": time_val}

    async def query(self, symbol: str, limit: int = 100) -> List[Dict[str, Any]]:
        results = []
        for table in self.TABLE_MAP.values():
            query = (
                f"SELECT * FROM {table} WHERE symbol = $1 ORDER BY time DESC LIMIT $2"
            )
            rows = await fetch(query, symbol, limit)
            results.extend(rows)
        results.sort(key=lambda x: x["time"], reverse=True)
        return results[:limit]

    async def get_stats(self) -> Dict[str, Any]:
        stats = {}
        for table in self.TABLE_MAP.values():
            count = await fetchrow(f"SELECT COUNT(*) FROM {table}")
            stats[table] = count[0] if count else 0
        return stats
