import logging

from runtime.base_engine import BaseRawEngine

logger = logging.getLogger(__name__)


class HealthMonitor:
    def get_health(self, engine: BaseRawEngine):
        try:
            return engine.health()
        except Exception as e:
            logger.error(f"Health check failed for {engine.name}: {e}")
            return {"status": "unhealthy", "error": str(e)}

    def get_all_health(self, engines):
        return {e.name: self.get_health(e) for e in engines}
