"""Universal COT Parser – institutional-grade with full field extraction."""

import csv
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from pathlib import Path

logger = logging.getLogger(__name__)


class COTParser:
    """Universal CFTC COT parser – parses every market and all fields."""

    def __init__(self):
        self.market_registry = {}
        self.field_mappings = self._get_field_mappings()

    def _get_field_mappings(self) -> Dict[str, str]:
        """Return field name mappings for CFTC CSV."""
        return {
            # Market identification
            "Market and Exchange Names": "market_name",
            "Report Date": "report_date",
            # Open Interest
            "Open Interest (All)": "open_interest",
            "Open Interest": "open_interest",
            # Dealer positions
            "Dealer Long": "dealer_long",
            "Dealer Short": "dealer_short",
            "Dealer Spreading": "dealer_spreading",
            "Dealer Long Change": "dealer_chg_long",
            "Dealer Short Change": "dealer_chg_short",
            "Dealer Spreading Change": "dealer_chg_spread",
            "Dealer Percent of OI": "dealer_pct_oi",
            "Dealer Traders": "dealer_traders",
            # Commercial positions
            "Commercial Long": "commercial_long",
            "Commercial Short": "commercial_short",
            "Commercial Spreading": "commercial_spreading",
            "Commercial Long Change": "commercial_chg_long",
            "Commercial Short Change": "commercial_chg_short",
            "Commercial Spreading Change": "commercial_chg_spread",
            "Commercial Percent of OI": "commercial_pct_oi",
            "Commercial Traders": "commercial_traders",
            # Asset Manager positions
            "Asset Manager Long": "asset_manager_long",
            "Asset Manager Short": "asset_manager_short",
            "Asset Manager Spreading": "asset_manager_spreading",
            "Asset Manager Long Change": "asset_manager_chg_long",
            "Asset Manager Short Change": "asset_manager_chg_short",
            "Asset Manager Spreading Change": "asset_manager_chg_spread",
            "Asset Manager Percent of OI": "asset_manager_pct_oi",
            "Asset Manager Traders": "asset_manager_traders",
            # Leveraged Funds positions
            "Leveraged Funds Long": "leveraged_long",
            "Leveraged Funds Short": "leveraged_short",
            "Leveraged Funds Spreading": "leveraged_spreading",
            "Leveraged Funds Long Change": "leveraged_chg_long",
            "Leveraged Funds Short Change": "leveraged_chg_short",
            "Leveraged Funds Spreading Change": "leveraged_chg_spread",
            "Leveraged Funds Percent of OI": "leveraged_pct_oi",
            "Leveraged Funds Traders": "leveraged_traders",
            # Other Reportables
            "Other Reportables Long": "other_long",
            "Other Reportables Short": "other_short",
            "Other Reportables Long Change": "other_chg_long",
            "Other Reportables Short Change": "other_chg_short",
            "Other Reportables Percent of OI": "other_pct_oi",
            "Other Reportables Traders": "other_traders",
            # Nonreportables
            "Nonreportable Long": "nonreportable_long",
            "Nonreportable Short": "nonreportable_short",
            "Nonreportable Long Change": "nonreportable_chg_long",
            "Nonreportable Short Change": "nonreportable_chg_short",
            "Nonreportable Percent of OI": "nonreportable_pct_oi",
            "Nonreportable Traders": "nonreportable_traders",
        }

    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse a COT CSV file and extract all markets and fields."""
        if not Path(file_path).exists():
            logger.error(f"File not found: {file_path}")
            return []

        records = []
        try:
            with open(file_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record = self._extract_all_fields(row)
                    if record:
                        records.append(record)
                        self._discover_market(record)
            logger.info(f"Parsed {len(records)} records from {file_path}")
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
        return records

    def _extract_all_fields(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Extract all fields from a COT row."""
        try:
            record = {}
            for csv_field, internal_field in self.field_mappings.items():
                value = row.get(csv_field, "").strip()
                if value and value != "":
                    # Try to convert to int, keep as string if fails
                    try:
                        record[internal_field] = int(value.replace(",", ""))
                    except (ValueError, AttributeError):
                        record[internal_field] = value

            # Ensure market name is set
            if "market_name" not in record or not record["market_name"]:
                return None

            # Extract market code from name
            record["market_code"] = self._extract_market_code(record["market_name"])
            record["report_date"] = row.get(
                "Report Date", datetime.now().strftime("%Y-%m-%d")
            )

            return record
        except Exception as e:
            logger.warning(f"Failed to extract fields: {e}")
            return None

    def _extract_market_code(self, market_name: str) -> str:
        """Extract market code from market name."""
        # Common codes
        code_mapping = {
            "EURO FX": "EUR",
            "BRITISH POUND": "GBP",
            "JAPANESE YEN": "JPY",
            "SWISS FRANC": "CHF",
            "CANADIAN DOLLAR": "CAD",
            "AUSTRALIAN DOLLAR": "AUD",
            "NEW ZEALAND DOLLAR": "NZD",
            "MEXICAN PESO": "MXN",
            "GOLD": "XAU",
            "SILVER": "XAG",
            "COPPER": "HG",
            "PLATINUM": "PL",
            "PALLADIUM": "PA",
            "WTI CRUDE": "CL",
            "BRENT": "BZ",
            "NATURAL GAS": "NG",
            "S&P 500": "ES",
            "NASDAQ": "NQ",
            "DOW": "YM",
            "10-YEAR TREASURY": "ZN",
            "30-YEAR TREASURY": "ZB",
            "5-YEAR TREASURY": "ZF",
            "CORN": "C",
            "WHEAT": "W",
            "SOYBEANS": "S",
            "BITCOIN": "BTC",
            "ETHER": "ETH",
        }
        for name, code in code_mapping.items():
            if name in market_name.upper():
                return code
        # Use first 3 letters if no mapping found
        return market_name[:3].upper()

    def _discover_market(self, record: Dict[str, Any]) -> None:
        """Discover and register a market from parsed data."""
        market_code = record.get("market_code")
        if not market_code:
            return
        if market_code not in self.market_registry:
            self.market_registry[market_code] = {
                "market_code": market_code,
                "market_name": record.get("market_name", market_code),
                "first_seen": record.get("report_date"),
                "last_seen": record.get("report_date"),
                "asset_class": self._classify_market(
                    market_code, record.get("market_name", "")
                ),
            }
        else:
            self.market_registry[market_code]["last_seen"] = record.get("report_date")

    def _classify_market(self, market_code: str, market_name: str = "") -> str:
        """Classify market by asset class."""
        code = market_code.upper()
        name = market_name.upper()
        if (
            code in ["EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD", "MXN"]
            or "FX" in name
        ):
            return "forex"
        if (
            code in ["XAU", "XAG", "HG", "PL", "PA"]
            or "GOLD" in name
            or "SILVER" in name
        ):
            return "metals"
        if (
            code in ["CL", "BZ", "NG"]
            or "OIL" in name
            or "GAS" in name
            or "ENERGY" in name
        ):
            return "energy"
        if (
            code in ["ES", "NQ", "YM"]
            or "S&P" in name
            or "NASDAQ" in name
            or "DOW" in name
        ):
            return "index"
        if code in ["ZN", "ZB", "ZF", "ZT"] or "TREASURY" in name or "BOND" in name:
            return "bonds"
        if (
            code in ["C", "W", "S"]
            or "CORN" in name
            or "WHEAT" in name
            or "SOY" in name
        ):
            return "agriculture"
        if code in ["BTC", "ETH"]:
            return "crypto"
        return "other"

    def get_discovered_markets(self) -> Dict[str, Any]:
        """Return all discovered markets."""
        return self.market_registry
