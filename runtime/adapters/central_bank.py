import logging

from central_bank_engine.engine import CentralBankEngine
from runtime.base_engine import BaseRawEngine

logger = logging.getLogger(__name__)


class CentralBankEngineAdapter(BaseRawEngine):
    def __init__(self):
        self._engine = CentralBankEngine()
        self._initialized = False

    @property
    def name(self) -> str:
        return "central_bank"

    @property
    def enabled(self) -> bool:
        return True

    @property
    def interval_seconds(self) -> int:
        return 300

    async def initialize(self):
        if not self._initialized:
            logger.info("Initializing Central Bank Engine")
            self._initialized = True

    async def run(self):
        if not self._initialized:
            await self.initialize()
        logger.info("Running Central Bank Engine")
        return await self._engine.run()

    async def shutdown(self):
        logger.info("Shutting down Central Bank Engine")
        self._initialized = False

    def health(self):
        return {
            "status": "healthy" if self._initialized else "not_initialized",
            "engine": "central_bank",
        }

    def metrics(self):
        return {"engine": "central_bank", "last_run": "N/A", "collected": 0}
