"""Publication Router – directs normalized data to the correct warehouse."""

import logging
from typing import Any, Dict

from ndip.warehouses.price.warehouse import PriceWarehouse

logger = logging.getLogger(__name__)


class PublicationRouter:
    """Routes data to the appropriate warehouse based on asset_class."""

    # Map asset_class -> warehouse instance
    WAREHOUSE_MAP = {
        "forex": PriceWarehouse,
        "commodity": PriceWarehouse,
        "index": PriceWarehouse,
        "equity": PriceWarehouse,
        "crypto": PriceWarehouse,
        # Later we'll add: "macro", "institutional", etc.
    }

    def __init__(self):
        self._warehouses = {}

    def _get_warehouse(self, asset_class: str):
        """Get or create a warehouse instance for the asset_class."""
        if asset_class not in self.WAREHOUSE_MAP:
            raise ValueError(f"No warehouse configured for asset_class: {asset_class}")
        if asset_class not in self._warehouses:
            self._warehouses[asset_class] = self.WAREHOUSE_MAP[asset_class]()
        return self._warehouses[asset_class]

    async def route(self, record: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Route a single record to its warehouse."""
        asset_class = record.get("asset_class", "unknown")
        warehouse = self._get_warehouse(asset_class)
        result = await warehouse.store(record, source)
        return result
