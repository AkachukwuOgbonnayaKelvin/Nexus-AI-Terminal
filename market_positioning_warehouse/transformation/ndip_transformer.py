"""NDIP Transformer – Creates asset-specific position collections."""

import logging

from market_positioning_warehouse.classification import AssetClassifier
from market_positioning_warehouse.publication import NDIPPublisher
from market_positioning_warehouse.warehouse import Repository

logger = logging.getLogger(__name__)


class NDIPTransformer:
    """Transforms raw positions into asset-specific NDIP collections."""

    def __init__(self):
        self.repository = Repository()
        self.classifier = AssetClassifier()
        self.publisher = NDIPPublisher()

    async def transform_and_publish(self, limit: int = 1000) -> dict[str, int]:
        """Transform raw positions and publish to NDIP."""
        positions = await self.repository.get_unprocessed(limit)

        by_asset_class = {}
        for position in positions:
            classification = self.classifier.classify(position.market_name)
            asset_class = classification.get("asset_class", "unknown")

            if asset_class not in by_asset_class:
                by_asset_class[asset_class] = []
            by_asset_class[asset_class].append(position)

        published = 0
        for asset_class, positions in by_asset_class.items():
            count = await self.publisher.publish_collection(asset_class, positions)
            published += count

        return {"published": published, "asset_classes": len(by_asset_class)}
