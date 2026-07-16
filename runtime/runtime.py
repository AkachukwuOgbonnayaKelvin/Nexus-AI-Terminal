#!/usr/bin/env python3
"""Data Acquisition Runtime (DAR-001)."""

import asyncio
import logging
import signal
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from runtime.engine_registry import register_engines, registry
from runtime.health import HealthMonitor
from runtime.metrics import metrics
from runtime.scheduler import Scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class Runtime:
    """Main runtime orchestrator."""

    def __init__(self):
        self.scheduler = Scheduler()
        self.health_monitor = HealthMonitor()
        self.running = True

    async def health_loop(self, engines):
        """Periodically log health status."""
        while self.running:
            await asyncio.sleep(60)
            health = self.health_monitor.get_all_health(engines)
            logger.info(f"Health: {health}")

    async def metrics_loop(self, engines):
        """Periodically log metrics."""
        while self.running:
            await asyncio.sleep(300)  # every 5 minutes
            all_metrics = metrics.get_all_metrics(engines)
            for name, m in all_metrics.items():
                logger.info(
                    f"Metrics {name}: runs={m['runs']}, errors={m['errors']}, avg_duration={m['avg_duration_ms']:.2f}ms"
                )

    async def run(self):
        """Start the runtime."""
        logger.info("Starting Nexus Data Acquisition Runtime (DAR-001)")

        # Register engines
        register_engines()
        engines = registry.get_enabled()
        logger.info(f"Registered {len(engines)} engines: {[e.name for e in engines]}")

        # Start health and metrics loops
        health_task = asyncio.create_task(self.health_loop(engines))
        metrics_task = asyncio.create_task(self.metrics_loop(engines))

        # Run scheduler
        try:
            await self.scheduler.run_all(engines)
        except KeyboardInterrupt:
            logger.info("Shutdown requested")
        finally:
            self.running = False
            health_task.cancel()
            metrics_task.cancel()
            await asyncio.gather(health_task, metrics_task, return_exceptions=True)
            for engine in engines:
                await engine.shutdown()
            logger.info("Runtime shutdown complete")


def signal_handler(sig, frame):
    """Handle shutdown signals."""
    logger.info("Received shutdown signal")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    runtime = Runtime()
    asyncio.run(runtime.run())
