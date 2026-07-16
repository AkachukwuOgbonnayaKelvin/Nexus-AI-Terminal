import logging

from runtime.base_engine import BaseRawEngine

logger = logging.getLogger(__name__)


class Dispatcher:
    async def run_engine(self, engine: BaseRawEngine):
        try:
            if not engine.enabled:
                return {"status": "skipped", "reason": "disabled"}
            logger.info(f"Running {engine.name}...")
            result = await engine.run()
            logger.info(f"{engine.name} completed: {result}")
            return {"status": "success", "result": result}
        except Exception as e:
            logger.exception(f"{engine.name} failed: {e}")
            return {"status": "error", "error": str(e)}
