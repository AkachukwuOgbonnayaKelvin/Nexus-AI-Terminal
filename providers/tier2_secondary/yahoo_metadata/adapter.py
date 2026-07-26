from typing import Any

from providers.dtos.transport import UniversalTransport
from providers.interfaces.base_adapter import BaseAdapter


class YahooMetadataAdapter(BaseAdapter):
    def adapt(self, raw_data: dict[str, Any], source: str) -> UniversalTransport:
        # Not used for metadata; we store directly in MetadataWarehouse
        return None

    def adapt_batch(
        self, raw_data: list[dict[str, Any]], source: str
    ) -> list[UniversalTransport]:
        return []
