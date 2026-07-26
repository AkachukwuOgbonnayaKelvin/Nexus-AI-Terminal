"""TFF COT Report Parser."""

import logging
from typing import Any

from institutional_positioning_engine.parser.base_parser import BaseParser

logger = logging.getLogger(__name__)


class TFFParser(BaseParser):
    """Parser for Traders in Financial Futures (TFF) COT reports."""

    def get_report_type(self) -> str:
        return "tff"

    def parse(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Parse TFF COT data."""
        records = []

        for row in data:
            try:
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
                    # Dealer/Intermediary
                    "dealer_long": self._safe_int(
                        self._extract_field(row, "Dealer Long", "dealer_long")
                    ),
                    "dealer_short": self._safe_int(
                        self._extract_field(row, "Dealer Short", "dealer_short")
                    ),
                    "dealer_spread": self._safe_int(
                        self._extract_field(row, "Dealer Spread", "dealer_spread")
                    ),
                    # Asset Manager/Institutional
                    "asset_manager_long": self._safe_int(
                        self._extract_field(
                            row, "Asset Manager Long", "asset_manager_long"
                        )
                    ),
                    "asset_manager_short": self._safe_int(
                        self._extract_field(
                            row, "Asset Manager Short", "asset_manager_short"
                        )
                    ),
                    "asset_manager_spread": self._safe_int(
                        self._extract_field(
                            row, "Asset Manager Spread", "asset_manager_spread"
                        )
                    ),
                    # Leveraged Funds
                    "leveraged_long": self._safe_int(
                        self._extract_field(
                            row, "Leveraged Funds Long", "leveraged_long"
                        )
                    ),
                    "leveraged_short": self._safe_int(
                        self._extract_field(
                            row, "Leveraged Funds Short", "leveraged_short"
                        )
                    ),
                    "leveraged_spread": self._safe_int(
                        self._extract_field(
                            row, "Leveraged Funds Spread", "leveraged_spread"
                        )
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
                }

                if record.get("market_name"):
                    records.append(record)

            except Exception as e:
                logger.warning(f"Failed to parse TFF row: {e}")
                continue

        logger.info(f"Parsed {len(records)} TFF records")
        return records
