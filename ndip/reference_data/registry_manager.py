import logging
from typing import Any, Dict, Optional

from ndip.utils.db_connector import fetchrow

logger = logging.getLogger(__name__)


class RegistryManager:
    def __init__(self):
        self.cache = {}

    async def lookup(self, table: str, unique_field: str, value: str) -> Optional[Dict[str, Any]]:
        cache_key = f"{table}:{unique_field}:{value}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        query = f"SELECT * FROM metadata.{table} WHERE {unique_field} = $1"
        row = await fetchrow(query, value)
        if row:
            record = dict(row)
            self.cache[cache_key] = record
            return record
        return None

    async def insert(self, table: str, record: Dict[str, Any]) -> Dict[str, Any]:
        pk = await self._get_primary_key(table)
        columns = list(record.keys())
        placeholders = [f"${i + 1}" for i in range(len(columns))]
        query = f"""
            INSERT INTO metadata.{table} ({", ".join(columns)})
            VALUES ({", ".join(placeholders)})
            RETURNING {pk}
        """
        result = await fetchrow(query, *[record[c] for c in columns])
        inserted_record = {pk: result[pk]}
        inserted_record.update(record)
        self.cache = {k: v for k, v in self.cache.items() if not k.startswith(f"{table}:")}
        return inserted_record

    async def _get_primary_key(self, table: str) -> str:
        mapping = {
            "exchange_registry": "mic_code",
            "currency_registry": "code",
            "country_registry": "code",
            "sector_registry": "sector_id",
            "industry_registry": "industry_id",
            "company_registry": "company_id",
            "asset_type_registry": "asset_type_id",
        }
        return mapping.get(table, "id")
