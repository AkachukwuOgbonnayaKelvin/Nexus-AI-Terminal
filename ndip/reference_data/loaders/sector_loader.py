from .base_loader import BaseLoader


class SectorLoader(BaseLoader):
    def __init__(self, registry_manager):
        super().__init__(registry_manager, "sector_registry", "name")

    async def _prepare_record(self, value: str, source: str, metadata: dict) -> dict:
        return {"name": value}
