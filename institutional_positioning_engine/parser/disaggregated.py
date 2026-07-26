"""Disaggregated COT Report Parser."""

import logging
from typing import Any

from institutional_positioning_engine.parser.base_parser import BaseParser

logger = logging.getLogger(__name__)


class DisaggregatedParser(BaseParser):
    """Parser for Disaggregated COT reports."""

    def get_report_type(self) -> str:
        return "disaggregated"

    def parse(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Parse disaggregated COT data."""
        records = []

        for row in data:
            try:
                # Extract market name
                market_name = self._extract_field(
                    row,
                    "Market and Exchange Names",
                    "market_name",
                    "Contract Market Name",
                    "market",
                )
                if not market_name:
                    continue

                record = {
                    "market_name": market_name,
                    "report_date": self._extract_field(
                        row, "Report Date", "report_date"
                    ),
                    "market_code": self._extract_field(
                        row, "market_code", "Contract Market Code"
                    ),
                    "open_interest": self._safe_int(
                        self._extract_field(row, "Open Interest", "open_interest")
                    ),
                    # Producer/Merchant/Processor/User
                    "prod_long": self._safe_int(
                        self._extract_field(row, "Producer Long", "prod_long")
                    ),
                    "prod_short": self._safe_int(
                        self._extract_field(row, "Producer Short", "prod_short")
                    ),
                    "prod_spread": self._safe_int(
                        self._extract_field(row, "Producer Spread", "prod_spread")
                    ),
                    # Swap Dealers
                    "swap_long": self._safe_int(
                        self._extract_field(row, "Swap Long", "swap_long")
                    ),
                    "swap_short": self._safe_int(
                        self._extract_field(row, "Swap Short", "swap_short")
                    ),
                    "swap_spread": self._safe_int(
                        self._extract_field(row, "Swap Spread", "swap_spread")
                    ),
                    # Managed Money
                    "money_long": self._safe_int(
                        self._extract_field(row, "Managed Money Long", "money_long")
                    ),
                    "money_short": self._safe_int(
                        self._extract_field(row, "Managed Money Short", "money_short")
                    ),
                    "money_spread": self._safe_int(
                        self._extract_field(row, "Managed Money Spread", "money_spread")
                    ),
                    # Other Reportables
                    "other_long": self._safe_int(
                        self._extract_field(row, "Other Reportables Long", "other_long")
                    ),
                    "other_short": self._safe_int(
                        self._extract_field(
                            row, "Other Reportables Short", "other_short"
                        )
                    ),
                    # Nonreportables
                    "nonrep_long": self._safe_int(
                        self._extract_field(row, "Nonreportable Long", "nonrep_long")
                    ),
                    "nonrep_short": self._safe_int(
                        self._extract_field(row, "Nonreportable Short", "nonrep_short")
                    ),
                }

                # Only add if we have market_name
                if record.get("market_name"):
                    records.append(record)

            except Exception as e:
                logger.warning(f"Failed to parse disaggregated row: {e}")
                continue

        logger.info(f"Parsed {len(records)} disaggregated records")
        return records
