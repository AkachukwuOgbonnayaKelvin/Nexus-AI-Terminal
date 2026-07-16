import logging
from typing import Optional

from ndip.reference_data.registry_manager import RegistryManager

logger = logging.getLogger(__name__)


class BaseLoader:
    def __init__(
        self, registry_manager: RegistryManager, table: str, unique_field: str
    ):
        self.registry = registry_manager
        self.table = table
        self.unique_field = unique_field

    async def ensure(self, value: str, source: str, metadata: dict) -> Optional[str]:
        if not value:
            return None
        existing = await self.registry.lookup(self.table, self.unique_field, value)
        if existing:
            pk = await self.registry._get_primary_key(self.table)
            return existing.get(pk)
        record = await self._prepare_record(value, source, metadata)
        inserted = await self.registry.insert(self.table, record)
        pk = await self.registry._get_primary_key(self.table)
        return inserted.get(pk)

    async def _prepare_record(self, value: str, source: str, metadata: dict) -> dict:
        return {self.unique_field: value}
