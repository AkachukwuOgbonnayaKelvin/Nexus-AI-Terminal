"""Historical Loader – Loads CFTC historical data from official archives."""

import io
import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests

logger = logging.getLogger(__name__)


class HistoricalLoader:
    """Loads historical CFTC data from compressed archives."""

    def __init__(self):
        self.base_url = "https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed"
        self.years = range(1986, datetime.now().year + 1)

    def load_year(self, year: int) -> List[Dict[str, Any]]:
        """Load a single year's data."""
        records = []
        logger.info(f"Loading data for {year}...")

        # Try different file formats
        formats = [
            (f"{self.base_url}/cot_{year}.csv", self._parse_csv),
            (f"{self.base_url}/cot_{year}.xlsx", self._parse_excel),
            (f"{self.base_url}/cot_{year}.zip", self._parse_zip),
        ]

        for url, parser in formats:
            try:
                response = requests.get(url, timeout=60)
                if response.status_code == 200:
                    records = parser(response.content)
                    if records:
                        logger.info(f"Loaded {len(records)} records from {year}")
                        return records
            except Exception as e:
                logger.debug(f"Format failed for {year}: {e}")
                continue

        logger.warning(f"No data found for {year}")
        return records

    def _parse_csv(self, content: bytes) -> List[Dict[str, Any]]:
        """Parse CSV content."""
        try:
            df = pd.read_csv(io.BytesIO(content))
            return df.to_dict("records")
        except Exception as e:
            logger.warning(f"CSV parse failed: {e}")
            return []

    def _parse_excel(self, content: bytes) -> List[Dict[str, Any]]:
        """Parse Excel content."""
        try:
            df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
            return df.to_dict("records")
        except Exception as e:
            logger.warning(f"Excel parse failed: {e}")
            return []

    def _parse_zip(self, content: bytes) -> List[Dict[str, Any]]:
        """Parse ZIP content."""
        import zipfile

        records = []
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as zf:
                for filename in zf.namelist():
                    if filename.endswith(".csv"):
                        with zf.open(filename) as f:
                            df = pd.read_csv(f)
                            records.extend(df.to_dict("records"))
            return records
        except Exception as e:
            logger.warning(f"ZIP parse failed: {e}")
            return []
