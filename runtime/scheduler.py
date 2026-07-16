import asyncio
import logging
import time
from typing import List

from runtime.base_engine import BaseRawEngine
from runtime.dispatcher import Dispatcher
from runtime.metrics import metrics

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.dispatcher = Dispatcher()

    async def run_engine_loop(self, engine: BaseRawEngine):
        while True:
            start = time.time()
            result = await self.dispatcher.run_engine(engine)
            duration = time.time() - start
            success = result.get("status") == "success"
            metrics.record_run(engine.name, success, duration)
            if not success:
                logger.warning(f"{engine.name} failed, will retry next cycle")
            await asyncio.sleep(engine.interval_seconds)

    async def run_all(self, engines: List[BaseRawEngine]):
        tasks = []
        for engine in engines:
            if engine.enabled:
                task = asyncio.create_task(self.run_engine_loop(engine))
                tasks.append(task)
            else:
                logger.info(f"Engine {engine.name} is disabled, skipping")
        await asyncio.gather(*tasks)
