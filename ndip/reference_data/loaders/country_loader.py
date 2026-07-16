from .base_loader import BaseLoader


class CountryLoader(BaseLoader):
    def __init__(self, registry_manager):
        super().__init__(registry_manager, "country_registry", "code")

    async def _prepare_record(self, value: str, source: str, metadata: dict) -> dict:
        return {"code": value, "name": value}
