import json
import logging

from macroeconomic_events_engine.dtos import UniversalMacroEvent
from ndip.utils.db_connector import execute

logger = logging.getLogger(__name__)


class RawWarehouse:
    def __init__(self):
        self.table = "macro_events_raw"

    async def store(self, event: UniversalMacroEvent, provider: str) -> bool:
        query = f"""
            INSERT INTO {self.table} (provider, provider_event_id, country, currency,
                title, category, forecast, previous, actual, importance,
                release_time_utc, status, raw_data)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
        """
        try:
            await execute(
                query,
                provider,
                event.provider_event_id,
                event.country,
                event.currency,
                event.title,
                event.category,
                event.forecast,
                event.previous,
                event.actual,
                event.importance,
                event.release_time_utc,
                event.status,
                json.dumps(event.metadata),
            )
            return True
        except Exception as e:
            logger.error(f"Raw store error: {e}")
            return False
