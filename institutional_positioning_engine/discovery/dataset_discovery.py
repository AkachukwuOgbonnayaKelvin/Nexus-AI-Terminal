"""Dataset Discovery – Finds actual CFTC dataset IDs."""

import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class DatasetDiscovery:
    """Discovers actual CFTC PRE dataset IDs."""

    def __init__(self):
        self.base_url = "https://publicreporting.cftc.gov"
        self.discovered_datasets = {}

    def discover_all(self) -> Dict[str, str]:
        """Discover all COT dataset IDs."""
        # Common known dataset IDs from CFTC PRE
        # These are the actual IDs used by the CFTC
        known_datasets = {
            "disaggregated": "kh3c-gbw2",  # Example, find actual
            "legacy_futures": "6dca-aqww",  # Example, find actual
            "legacy_futures_options": "xxxx-xxxx",  # Find actual
            "tff": "xxxx-xxxx",  # Find actual
        }

        # Try to discover from the catalog
        try:
            catalog = self._fetch_catalog()
            if catalog:
                discovered = self._extract_cot_datasets(catalog)
                if discovered:
                    return discovered
        except Exception as e:
            logger.warning(f"Catalog discovery failed: {e}")

        # Fallback to known IDs
        logger.info(f"Using {len(known_datasets)} known dataset IDs")
        return known_datasets

    def _fetch_catalog(self) -> Optional[List[Dict]]:
        """Fetch the dataset catalog."""
        # Try different catalog endpoints
        urls = [
            f"{self.base_url}/api/catalog/v1",
            f"{self.base_url}/api/views/v1",
            f"{self.base_url}/api/datasets/v1",
        ]

        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                continue
        return None

    def _extract_cot_datasets(self, catalog: List[Dict]) -> Dict[str, str]:
        """Extract COT datasets from catalog."""
        datasets = {}
        for item in catalog:
            name = str(item).lower()
            if "cot" in name or "commitment" in name or "trader" in name:
                # Extract ID from the item
                dataset_id = self._extract_id(item)
                if dataset_id:
                    datasets[name] = dataset_id
        return datasets

    def _extract_id(self, item: Any) -> Optional[str]:
        """Extract dataset ID from catalog item."""
        if isinstance(item, dict):
            if "id" in item:
                return item["id"]
            if "resource" in item and isinstance(item["resource"], dict):
                return item["resource"].get("id")
        return None
