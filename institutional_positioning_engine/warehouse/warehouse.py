"""COT Warehouse – institutional-grade storage."""

import logging
from typing import Any, Dict

from ndip.utils.db_connector import execute, fetchrow

logger = logging.getLogger(__name__)


class COTWarehouse:
    def __init__(self):
        self.market_table = "cot_market_registry"
        self.report_table = "cot_reports"
        self.position_table = "cot_positions"

    def store(self, record: Dict[str, Any]) -> bool:
        """Store a parsed COT record."""
        try:
            query = f"""
                INSERT INTO {self.position_table} (
                    market_code, market_name, report_date,
                    open_interest,
                    dealer_long, dealer_short, dealer_spreading,
                    commercial_long, commercial_short, commercial_spreading,
                    asset_manager_long, asset_manager_short, asset_manager_spreading,
                    leveraged_long, leveraged_short, leveraged_spreading,
                    other_long, other_short,
                    nonreportable_long, nonreportable_short,
                    total_traders
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21)
                ON CONFLICT (market_code, report_date) DO UPDATE SET
                    open_interest = EXCLUDED.open_interest,
                    dealer_long = EXCLUDED.dealer_long,
                    dealer_short = EXCLUDED.dealer_short,
                    updated_at = NOW()
            """
            execute(
                query,
                record.get("market_code"),
                record.get("market_name"),
                record.get("report_date"),
                record.get("open_interest"),
                record.get("dealer_long"),
                record.get("dealer_short"),
                record.get("dealer_spreading"),
                record.get("commercial_long"),
                record.get("commercial_short"),
                record.get("commercial_spreading"),
                record.get("asset_manager_long"),
                record.get("asset_manager_short"),
                record.get("asset_manager_spreading"),
                record.get("leveraged_long"),
                record.get("leveraged_short"),
                record.get("leveraged_spreading"),
                record.get("other_long"),
                record.get("other_short"),
                record.get("nonreportable_long"),
                record.get("nonreportable_short"),
                record.get("total_traders"),
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store record: {e}")
            return False

    def register_market(self, market: Dict[str, Any]) -> None:
        """Register a discovered market."""
        try:
            query = f"""
                INSERT INTO {self.market_table} (market_code, market_name, asset_class, first_seen, last_seen)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (market_code) DO UPDATE SET
                    last_seen = EXCLUDED.last_seen,
                    is_active = TRUE
            """
            execute(
                query,
                market.get("market_code"),
                market.get("market_name"),
                market.get("asset_class"),
                market.get("first_seen"),
                market.get("last_seen"),
            )
        except Exception as e:
            logger.error(f"Failed to register market: {e}")

    async def has_data(self) -> bool:
        """Check if warehouse already has data."""
        try:
            query = f"SELECT COUNT(*) FROM {self.report_table}"
            row = await fetchrow(query)
            return row[0] > 0 if row else False
        except Exception:
            return False
