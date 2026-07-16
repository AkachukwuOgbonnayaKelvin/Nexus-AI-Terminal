from .base_loader import BaseLoader


class AssetTypeLoader(BaseLoader):
    def __init__(self, registry_manager):
        super().__init__(registry_manager, "asset_type_registry", "name")

    async def _prepare_record(self, value: str, source: str, metadata: dict) -> dict:
        asset_class = metadata.get("asset_class", "unknown")
        return {"name": value, "asset_class": asset_class}
