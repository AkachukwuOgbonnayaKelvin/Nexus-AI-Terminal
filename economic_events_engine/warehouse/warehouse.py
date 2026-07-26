import json
import logging

from economic_events_engine.dtos import UniversalEconomicEvent
from ndip.utils.db_connector import execute, fetchrow

logger = logging.getLogger(__name__)


class EconomicWarehouse:
    def __init__(self):
        self.table = "economic_events"

    async def store_event(self, event: UniversalEconomicEvent) -> bool:
        query = f"""
            INSERT INTO {self.table} (
                event_id, provider, provider_event_id, country, region, currency,
                title, short_title, category, subcategory,
                forecast, previous, actual, consensus, revised_previous,
                importance, release_time_utc, release_time_local, timezone,
                frequency, status, source_url,
                tags, affected_assets, affected_markets,
                confidence, quality_score, metadata
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
                      $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28)
            ON CONFLICT (event_id, release_time_utc) DO UPDATE SET
                provider = EXCLUDED.provider,
                provider_event_id = EXCLUDED.provider_event_id,
                country = EXCLUDED.country,
                region = EXCLUDED.region,
                currency = EXCLUDED.currency,
                title = EXCLUDED.title,
                short_title = EXCLUDED.short_title,
                category = EXCLUDED.category,
                subcategory = EXCLUDED.subcategory,
                forecast = EXCLUDED.forecast,
                previous = EXCLUDED.previous,
                actual = EXCLUDED.actual,
                consensus = EXCLUDED.consensus,
                revised_previous = EXCLUDED.revised_previous,
                importance = EXCLUDED.importance,
                release_time_local = EXCLUDED.release_time_local,
                timezone = EXCLUDED.timezone,
                frequency = EXCLUDED.frequency,
                status = EXCLUDED.status,
                source_url = EXCLUDED.source_url,
                tags = EXCLUDED.tags,
                affected_assets = EXCLUDED.affected_assets,
                affected_markets = EXCLUDED.affected_markets,
                confidence = EXCLUDED.confidence,
                quality_score = EXCLUDED.quality_score,
                metadata = EXCLUDED.metadata,
                created_at = NOW()
        """
        try:
            await execute(
                query,
                event.event_id,
                event.provider,
                event.provider_event_id,
                event.country,
                event.region,
                event.currency,
                event.title,
                event.short_title,
                event.category,
                event.subcategory,
                event.forecast,
                event.previous,
                event.actual,
                event.consensus,
                event.revised_previous,
                event.importance,
                event.release_time_utc,
                event.release_time_local,
                event.timezone,
                event.frequency,
                event.status,
                event.source_url,
                event.tags,
                event.affected_assets,
                event.affected_markets,
                event.confidence,
                event.quality_score,
                json.dumps(event.metadata),
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store event {event.event_id}: {e}")
            return False

    # ... rest of the query methods (unchanged) ...

    async def get_latest_value(self, series_id: str) -> dict | None:
        """Get the latest value for a series."""
        query = f"SELECT * FROM {self.table} WHERE provider_event_id = $1 ORDER BY release_time_utc DESC LIMIT 1"
        row = await fetchrow(query, series_id)
        return dict(row) if row else None
