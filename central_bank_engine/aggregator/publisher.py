"""Publisher – stores normalized events directly into the central bank warehouse."""

import logging
from typing import Any, Dict, List

from central_bank_engine.dtos import UniversalCentralBankEvent
from central_bank_engine.warehouse.event_warehouse import CentralBankWarehouse

logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self):
        self.warehouse = CentralBankWarehouse()

    async def publish(self, events: List[UniversalCentralBankEvent]) -> List[Dict[str, Any]]:
        results = []
        for event in events:
            try:
                result = await self.warehouse.store(event)
                results.append(
                    {
                        "event_id": event.event_id,
                        "success": result,
                    }
                )
                if result:
                    logger.info(f"✅ Published event {event.event_id} ({event.bank} - {event.event_type})")
                else:
                    logger.error(f"❌ Failed to publish event {event.event_id}")
            except Exception as e:
                logger.exception(f"Exception publishing {event.event_id}: {e}")
                results.append(
                    {
                        "event_id": event.event_id,
                        "success": False,
                        "error": str(e),
                    }
                )
        return results
