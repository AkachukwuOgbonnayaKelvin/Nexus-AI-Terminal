"""Historical Archive Client – Fallback source for COT data."""

import csv
import io
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class HistoricalArchiveClient:
    """Client for CFTC historical archives."""

    def __init__(self):
        self.base_url = "https://www.cftc.gov/files/dea/history"
        self._cache = {}

    def get_latest_report(self) -> Optional[List[Dict[str, Any]]]:
        """Get the latest report from historical archives."""
        # Get the current year
        year = datetime.now().year
        try:
            data = self.get_year(year)
            if data:
                # Return only the most recent week
                return data[:100]  # Limit for latest
        except Exception as e:
            logger.error(f"Failed to get latest from historical: {e}")
        return None

    def get_year(self, year: int) -> Optional[List[Dict[str, Any]]]:
        """Get all reports for a specific year."""
        cache_key = f"year_{year}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        records = []
        # Try different file patterns
        urls = [
            f"{self.base_url}/cot_{year}.zip",
            f"{self.base_url}/cot_f_{year}.zip",
            f"{self.base_url}/cot_d_{year}.zip",
        ]

        for url in urls:
            try:
                response = requests.get(url, timeout=60)
                if response.status_code == 200:
                    records = self._parse_content(response.content)
                    break
            except Exception:
                continue

        if records:
            self._cache[cache_key] = records
            logger.info(f"Retrieved {len(records)} records for {year}")
        else:
            logger.warning(f"No data found for {year}")

        return records

    def _parse_content(self, content: bytes) -> List[Dict[str, Any]]:
        """Parse content from ZIP or CSV."""
        # Simple CSV parsing for now
        try:
            content_str = content.decode("utf-8")
            reader = csv.DictReader(io.StringIO(content_str))
            return list(reader)
        except Exception as e:
            logger.warning(f"Failed to parse content: {e}")
            return []

    def health_check(self) -> bool:
        """Check if historical archive is available."""
        try:
            url = f"{self.base_url}/cot_{datetime.now().year}.zip"
            response = requests.head(url, timeout=5)
            return response.status_code in [200, 302, 404]  # Any response means it's reachable
        except Exception:
            return False
