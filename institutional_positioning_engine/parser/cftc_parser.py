"""CFTC COT Parser – Parses the comma-delimited text files."""

import csv
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from pathlib import Path

logger = logging.getLogger(__name__)


class CFTCOTParser:
    """Parser for CFTC COT comma-delimited text files."""

    # Field mappings based on CFTC documentation
    FIELD_MAPPINGS = {
        "market_name": 0,
        "report_date_code": 1,
        "report_date": 2,
        "market_code": 3,
        "exchange": 4,
        "commodity_code": 5,
        "open_interest": 6,  # Position may vary
        # Commercial positions
        "commercial_long": 7,
        "commercial_short": 8,
        "commercial_spreading": 9,
        # Non-commercial positions
        "non_commercial_long": 10,
        "non_commercial_short": 11,
        "non_commercial_spreading": 12,
        # Other reportable positions
        "other_reportable_long": 13,
        "other_reportable_short": 14,
        # Non-reportable positions
        "non_reportable_long": 15,
        "non_reportable_short": 16,
        # Total positions
        "total_long": 17,
        "total_short": 18,
        # Changes
        "change_open_interest": 19,
        "change_commercial_long": 20,
        "change_commercial_short": 21,
        "change_non_commercial_long": 22,
        "change_non_commercial_short": 23,
        # Percentages
        "pct_commercial_long": 24,
        "pct_commercial_short": 25,
        "pct_non_commercial_long": 26,
        "pct_non_commercial_short": 27,
        # Trader counts
        "traders_commercial": 28,
        "traders_non_commercial": 29,
        # Additional fields for Long Format
        "crop_year": 30,
        "concentration_4_long": 31,
        "concentration_4_short": 32,
        "concentration_8_long": 33,
        "concentration_8_short": 34,
        "concentration_4_net_long": 35,
        "concentration_4_net_short": 36,
        "concentration_8_net_long": 37,
        "concentration_8_net_short": 38,
    }

    def parse_file(self, file_path: str, report_type: str = "disaggregated") -> List[Dict[str, Any]]:
        """Parse a CFTC COT file."""
        records = []
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    record = self._parse_row(row, report_type)
                    if record:
                        records.append(record)
            logger.info(f"Parsed {len(records)} records from {file_path}")
            return records
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return []

    def _parse_row(self, row: List[str], report_type: str) -> Optional[Dict[str, Any]]:
        """Parse a single row."""
        try:
            # Extract market name (quoted)
            market_name = row[0].strip('"')
            record = {
                "market_name": market_name,
                "report_date": row[2] if len(row) > 2 else None,
                "market_code": row[3] if len(row) > 3 else None,
                "open_interest": self._safe_int(row[6]) if len(row) > 6 else None,
            }

            # Add positions based on report type
            if report_type == "disaggregated":
                record.update(self._parse_disaggregated(row))
            elif report_type == "legacy":
                record.update(self._parse_legacy(row))

            return record
        except Exception as e:
            logger.warning(f"Failed to parse row: {e}")
            return None

    def _parse_disaggregated(self, row: List[str]) -> Dict[str, Any]:
        """Parse Disaggregated report format."""
        return {
            # Producer/Merchant/Processor/User
            "prod_long": self._safe_int(row[7]) if len(row) > 7 else None,
            "prod_short": self._safe_int(row[8]) if len(row) > 8 else None,
            "prod_spread": self._safe_int(row[9]) if len(row) > 9 else None,
            # Swap Dealers
            "swap_long": self._safe_int(row[10]) if len(row) > 10 else None,
            "swap_short": self._safe_int(row[11]) if len(row) > 11 else None,
            "swap_spread": self._safe_int(row[12]) if len(row) > 12 else None,
            # Managed Money
            "money_long": self._safe_int(row[13]) if len(row) > 13 else None,
            "money_short": self._safe_int(row[14]) if len(row) > 14 else None,
            "money_spread": self._safe_int(row[15]) if len(row) > 15 else None,
            # Other Reportables
            "other_long": self._safe_int(row[16]) if len(row) > 16 else None,
            "other_short": self._safe_int(row[17]) if len(row) > 17 else None,
            # Nonreportable
            "nonrep_long": self._safe_int(row[18]) if len(row) > 18 else None,
            "nonrep_short": self._safe_int(row[19]) if len(row) > 19 else None,
            # Changes
            "chg_oi": self._safe_int(row[20]) if len(row) > 20 else None,
        }

    def _parse_legacy(self, row: List[str]) -> Dict[str, Any]:
        """Parse Legacy report format."""
        return {
            "commercial_long": self._safe_int(row[7]) if len(row) > 7 else None,
            "commercial_short": self._safe_int(row[8]) if len(row) > 8 else None,
            "commercial_spread": self._safe_int(row[9]) if len(row) > 9 else None,
            "non_commercial_long": self._safe_int(row[10]) if len(row) > 10 else None,
            "non_commercial_short": self._safe_int(row[11]) if len(row) > 11 else None,
            "non_commercial_spread": self._safe_int(row[12]) if len(row) > 12 else None,
        }

    def _safe_int(self, value: Optional[str]) -> Optional[int]:
        """Safely convert a string to int."""
        if not value:
            return None
        try:
            return int(value.replace(",", "").strip())
        except ValueError:
            return None
