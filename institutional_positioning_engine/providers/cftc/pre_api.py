"""CFTC PRE API Client – Uses actual dataset IDs."""

import logging
from typing import Any, Dict, List, Optional

import requests

from institutional_positioning_engine.discovery.dataset_discovery import DatasetDiscovery

logger = logging.getLogger(__name__)


class PREAPIClient:
    """Client for CFTC PRE API."""

    def __init__(self):
        self.base_url = "https://publicreporting.cftc.gov/resource"
        self.discovery = DatasetDiscovery()
        self.datasets = self.discovery.discover_all()
        logger.info(f"Discovered {len(self.datasets)} datasets")

    def get_latest_report(self, report_type: str = "disaggregated") -> Optional[List[Dict[str, Any]]]:
        """Get the latest report for a specific type."""
        dataset_id = self.datasets.get(report_type)
        if not dataset_id:
            logger.warning(f"Unknown dataset type: {report_type}")
            return None

        url = f"{self.base_url}/{dataset_id}.json"
        params = {
            "$order": "report_date DESC",
            "$limit": 10000,
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data:
                    logger.info(f"Fetched {len(data)} records from {report_type}")
                    return data
            else:
                logger.warning(f"PRE API returned {response.status_code}")
        except Exception as e:
            logger.error(f"PRE API error: {e}")

        return None

    def health_check(self) -> bool:
        """Check if PRE API is available."""
        try:
            # Test with a known dataset
            dataset_id = self.datasets.get("disaggregated")
            if not dataset_id:
                return False
            url = f"{self.base_url}/{dataset_id}.json"
            params = {"$limit": 1}
            response = requests.get(url, params=params, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
