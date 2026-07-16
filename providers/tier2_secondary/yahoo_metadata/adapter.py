from typing import Any, Dict, List

from providers.dtos.transport import UniversalTransport
from providers.interfaces.base_adapter import BaseAdapter


class YahooMetadataAdapter(BaseAdapter):
    def adapt(self, raw_data: Dict[str, Any], source: str) -> UniversalTransport:
        # Not used for metadata; we store directly in MetadataWarehouse
        return None

    def adapt_batch(self, raw_data: List[Dict[str, Any]], source: str) -> List[UniversalTransport]:
        return []
