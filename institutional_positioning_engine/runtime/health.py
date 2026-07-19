"""COT Runtime Health – monitors the COT engine health."""

import logging
from datetime import datetime

from institutional_positioning_engine.runtime.state import COTRuntimeState

logger = logging.getLogger(__name__)


class COTRuntimeHealth:
    """Health monitor for the COT runtime."""

    def __init__(self):
        self.state = COTRuntimeState()

    async def check_health(self) -> dict:
        """Check the health of the COT runtime."""
        last_run = await self.state.get_last_run()
        last_report = await self.state.get_last_report()
        backfill_status = await self.state.get_backfill_status()

        health = {
            "status": "healthy",
            "last_run": last_run.isoformat() if last_run else None,
            "last_report": last_report,
            "backfill_complete": backfill_status.get("complete", False),
            "records_imported": backfill_status.get("records", 0),
        }

        # Check if we've missed a weekly update
        if last_run:
            days_since = (datetime.now() - last_run).days
            if days_since > 7:
                health["status"] = "warning"
                health["message"] = f"Missed weekly update ({days_since} days ago)"

        return health
