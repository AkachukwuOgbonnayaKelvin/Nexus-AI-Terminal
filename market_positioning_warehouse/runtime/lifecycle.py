"""Lifecycle Manager – Orchestrates the engine lifecycle."""

import logging
from datetime import datetime
from typing import Any

from market_positioning_warehouse.runtime.historical_import import HistoricalImport
from market_positioning_warehouse.runtime.repair_manager import RepairManager
from market_positioning_warehouse.runtime.weekly_scheduler import WeeklyScheduler
from market_positioning_warehouse.warehouse.state import WarehouseState

logger = logging.getLogger(__name__)


class LifecycleManager:
    """Manages the COT engine lifecycle."""

    def __init__(self):
        self.state = WarehouseState()
        self.historical = HistoricalImport()
        self.weekly = WeeklyScheduler()
        self.repair = RepairManager()

    async def run(self) -> dict[str, Any]:
        """Run the appropriate lifecycle stage."""
        logger.info("Checking warehouse state...")

        # Check if history exists
        history_complete = self.state.get("history_complete", False)

        if not history_complete:
            logger.info("Warehouse empty. Starting Historical Bootstrap...")
            result = await self.historical.run()
            self.state.mark_backfill_complete(
                start=str(result.get("years_processed")),
                end=str(datetime.now().year),
                records=result.get("records_inserted", 0),
            )
            return {"mode": "bootstrap", "result": result}

        # Check for missing reports
        missing = self.state.get("missing_reports", [])
        if missing:
            logger.info(f"Found {len(missing)} missing reports. Starting Repair...")
            result = await self.repair.run()
            return {"mode": "repair", "result": result}

        # Check if it's Friday
        now = datetime.now()
        if now.weekday() == 4:  # Friday
            logger.info("Friday detected. Running Weekly Update...")
            result = await self.weekly.run()
            if result.get("status") == "success":
                self.state.mark_update_complete(str(now.date()))
            return {"mode": "weekly", "result": result}

        # Idle state
        return {"mode": "idle", "message": "Not Friday, no missing reports"}
