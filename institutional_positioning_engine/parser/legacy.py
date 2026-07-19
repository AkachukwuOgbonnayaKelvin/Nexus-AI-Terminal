"""Legacy COT Report Parser."""

import logging
from typing import Any, Dict, List

from institutional_positioning_engine.parser.base_parser import BaseParser

logger = logging.getLogger(__name__)


class LegacyParser(BaseParser):
    """Parser for Legacy COT reports."""

    def get_report_type(self) -> str:
        return "legacy"

    def parse(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse legacy COT data."""
        records = []

        for row in data:
            try:
                market_name = self._extract_field(
                    row, "Market and Exchange Names", "market_name", "Contract Market Name", "market"
                )
                if not market_name:
                    continue

                record = {
                    "market_name": market_name,
                    "report_date": self._extract_field(row, "Report Date", "report_date"),
                    "market_code": self._extract_field(row, "market_code", "Contract Market Code"),
                    "open_interest": self._safe_int(self._extract_field(row, "Open Interest", "open_interest")),
                    # Commercial positions
                    "commercial_long": self._safe_int(self._extract_field(row, "Commercial Long", "commercial_long")),
                    "commercial_short": self._safe_int(
                        self._extract_field(row, "Commercial Short", "commercial_short")
                    ),
                    "commercial_spread": self._safe_int(
                        self._extract_field(row, "Commercial Spread", "commercial_spread")
                    ),
                    # Non-commercial positions
                    "non_commercial_long": self._safe_int(
                        self._extract_field(row, "Non-Commercial Long", "non_commercial_long")
                    ),
                    "non_commercial_short": self._safe_int(
                        self._extract_field(row, "Non-Commercial Short", "non_commercial_short")
                    ),
                    "non_commercial_spread": self._safe_int(
                        self._extract_field(row, "Non-Commercial Spread", "non_commercial_spread")
                    ),
                    # Nonreportables
                    "nonrep_long": self._safe_int(self._extract_field(row, "Nonreportable Long", "nonrep_long")),
                    "nonrep_short": self._safe_int(self._extract_field(row, "Nonreportable Short", "nonrep_short")),
                }

                if record.get("market_name"):
                    records.append(record)

            except Exception as e:
                logger.warning(f"Failed to parse legacy row: {e}")
                continue

        logger.info(f"Parsed {len(records)} legacy records")
        return records
