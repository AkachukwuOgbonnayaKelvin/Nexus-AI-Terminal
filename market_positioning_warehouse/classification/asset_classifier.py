"""Asset Classifier – Maps market names to asset classes."""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class AssetClassifier:
    """Classifies markets into asset classes."""

    def __init__(self, mapping_path: str = None):
        if mapping_path is None:
            mapping_path = Path(__file__).parent / "asset_mapping.yaml"
        self.mapping = self._load_mapping(mapping_path)

    def _load_mapping(self, path: Path) -> dict[str, Any]:
        """Load the asset mapping YAML file."""
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load mapping: {e}")
            return {"assets": {}}

    def classify(self, market_name: str) -> dict[str, str]:
        """Classify a market name."""
        if not market_name:
            return {"asset_class": "unknown", "subclass": "unknown", "symbol": "UNK"}

        market_name = market_name.strip().upper()
        assets = self.mapping.get("assets", {})

        # Try exact match
        for name, info in assets.items():
            if name in market_name:
                return {
                    "asset_class": info.get("asset_class", "unknown"),
                    "subclass": info.get("subclass", "unknown"),
                    "symbol": info.get("symbol", market_name[:3]),
                }

        # Try partial match
        for name, info in assets.items():
            if name in market_name or market_name in name:
                return {
                    "asset_class": info.get("asset_class", "unknown"),
                    "subclass": info.get("subclass", "unknown"),
                    "symbol": info.get("symbol", market_name[:3]),
                }

        return {
            "asset_class": "unknown",
            "subclass": "unknown",
            "symbol": market_name[:3],
        }
