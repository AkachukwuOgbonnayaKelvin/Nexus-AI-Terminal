from .base_loader import BaseLoader


class CompanyLoader(BaseLoader):
    def __init__(self, registry_manager):
        super().__init__(registry_manager, "company_registry", "name")

    async def _prepare_record(self, value: str, source: str, metadata: dict) -> dict:
        return {"name": value}
