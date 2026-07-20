"""Central Bank Publication Layer – publishes to NDIP."""

import logging

from central_bank_engine.dtos import UniversalCentralBankEvent
from central_bank_engine.warehouse import CentralBankWarehouse

logger = logging.getLogger(__name__)


class CentralBankPublisher:
    def __init__(self):
        self.warehouse = CentralBankWarehouse()

    async def publish(self, event: UniversalCentralBankEvent) -> bool:
        """Publish event to warehouse (and eventually NDIP)."""
        result = await self.warehouse.store(event)
        if result:
            logger.info(
                f"Published {event.event_id} ({event.bank} - {event.event_type})"
            )
        else:
            logger.error(f"Failed to publish {event.event_id}")
        return result
