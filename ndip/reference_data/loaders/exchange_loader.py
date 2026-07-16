from .base_loader import BaseLoader


class ExchangeLoader(BaseLoader):
    def __init__(self, registry_manager):
        super().__init__(registry_manager, "exchange_registry", "mic_code")

    async def _prepare_record(self, value: str, source: str, metadata: dict) -> dict:
        name = metadata.get("exchange_name", value)
        country = metadata.get("country", "")
        return {"mic_code": value, "name": name, "country": country}
