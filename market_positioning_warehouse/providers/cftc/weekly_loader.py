"""Weekly Loader – Loads current week's CFTC data from official sources."""

import logging
from datetime import datetime
from typing import Any

import requests

logger = logging.getLogger(__name__)


class WeeklyLoader:
    """Loads current week's CFTC data from official sources."""

    def __init__(self):
        self.sources = [
            ("https://www.cftc.gov/dea/newcot/FinFutWk.txt", "financial_futures"),
            ("https://www.cftc.gov/dea/newcot/FinComWk.txt", "financial_combined"),
            ("https://www.cftc.gov/dea/newcot/f_disagg.txt", "disaggregated_futures"),
            ("https://www.cftc.gov/dea/newcot/c_disagg.txt", "disaggregated_combined"),
        ]

    def load_current_week(self) -> list[dict[str, Any]]:
        """Load the current week's reports from all sources."""
        all_records = []
        for url, source_name in self.sources:
            try:
                records = self._fetch_txt(url, source_name)
                if records:
                    all_records.extend(records)
                    logger.info(f"Loaded {len(records)} records from {source_name}")
            except Exception as e:
                logger.warning(f"Failed to load {source_name}: {e}")
        return all_records

    def _fetch_txt(self, url: str, source_name: str) -> list[dict[str, Any]]:
        """Fetch and parse a TXT file from CFTC."""
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            logger.warning(f"Failed to fetch {url}: {response.status_code}")
            return []

        records = []
        lines = response.text.strip().split("\n")

        for line in lines:
            if not line.strip():
                continue

            # Try tab-separated first, then space-separated
            parts = line.split("\t")
            if len(parts) < 3:
                parts = line.split()

            if len(parts) >= 6:
                record = {
                    "market_name": parts[0].strip(),
                    "report_date": parts[2] if len(parts) > 2 else None,
                    "market_code": parts[3] if len(parts) > 3 else None,
                    "open_interest": self._safe_int(parts[6] if len(parts) > 6 else 0),
                    "source": source_name,
                    "fetched_at": datetime.now().isoformat(),
                }
                records.append(record)

        return records

    def _safe_int(self, value: Any) -> int | None:
        """Safely convert to int."""
        if value is None:
            return None
        try:
            if isinstance(value, str):
                return int(value.replace(",", "").strip())
            return int(value)
        except (ValueError, TypeError):
            return None
