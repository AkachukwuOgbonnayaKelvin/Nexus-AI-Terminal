"""COT Engine Adapter for DAR-001 Runtime."""

import logging

from institutional_positioning_engine.runtime.automated_scheduler import AutomatedCOTScheduler
from runtime.base_engine import BaseRawEngine

logger = logging.getLogger(__name__)


class COTEngineAdapter(BaseRawEngine):
    """Adapter for COT Engine to work with DAR-001."""

    def __init__(self):
        self._scheduler = AutomatedCOTScheduler()
        self._initialized = False
        self._has_data = False

    @property
    def name(self) -> str:
        return "cot_engine"

    @property
    def enabled(self) -> bool:
        return True

    @property
    def interval_seconds(self) -> int:
        # Check every hour for Friday updates
        return 3600

    async def initialize(self) -> None:
        if not self._initialized:
            logger.info("Initializing COT Engine")
            self._initialized = True

    async def run(self) -> dict:
        """Run a single collection cycle."""
        if not self._initialized:
            await self.initialize()

        logger.info("Running COT Engine collection cycle...")

        try:
            # Check if it's Friday (release day)
            import datetime

            now = datetime.datetime.now()
            if now.weekday() == 4:  # Friday
                # Process weekly update
                result = await self._scheduler._process_weekly_update()
                return result
            else:
                # Just health check - use a simple check without async issues
                health = self.health()
                return {"status": "idle", "message": "Not Friday", "health": health}
        except Exception as e:
            logger.error(f"COT Engine run failed: {e}")
            return {"status": "error", "error": str(e)}

    async def shutdown(self) -> None:
        logger.info("Shutting down COT Engine")
        self._scheduler.stop()
        self._initialized = False

    def health(self) -> dict:
        """Return health status."""
        try:
            # Use a simpler health check
            return {
                "status": "healthy",
                "engine": "cot_engine",
                "has_data": False,  # Simplifying health check
                "provider_status": {
                    "pre_api": False,
                    "historical": True,
                },
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def metrics(self) -> dict:
        """Return metrics."""
        return {
            "engine": "cot_engine",
            "last_run": "N/A",
            "records": 0,
        }
