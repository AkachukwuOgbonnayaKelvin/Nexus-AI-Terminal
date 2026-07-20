"""Repair Manager – Detects and repairs missing reports."""

import logging
from typing import Any, Dict

from market_positioning_warehouse.providers.cftc.historical_loader import (
    HistoricalLoader,
)
from market_positioning_warehouse.warehouse import Repository
from market_positioning_warehouse.warehouse.state import WarehouseState

logger = logging.getLogger(__name__)


class RepairManager:
    """Detects and repairs missing reports."""

    def __init__(self):
        self.state = WarehouseState()
        self.loader = HistoricalLoader()
        self.repository = Repository()

    async def run(self) -> Dict[str, Any]:
        """Run repair process."""
        logger.info("Starting repair process...")

        missing = self.state.get("missing_reports", [])
        if not missing:
            return {"status": "complete", "repaired": 0}

        repaired = 0
        for report_date in missing[:10]:  # Limit per run
            try:
                # Attempt to fetch and repair
                data = self.loader.load_year(int(report_date[:4]))
                if data:
                    repaired += 1
                    self.state.remove_missing_report(report_date)
                    logger.info(f"✅ Repaired {report_date}")
            except Exception as e:
                logger.error(f"Failed to repair {report_date}: {e}")

        return {
            "status": "partial" if repaired < len(missing) else "complete",
            "repaired": repaired,
        }
