import json
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from macroeconomic_events_engine.dtos import UniversalMacroEvent
from ndip.utils.db_connector import execute, fetch, fetchrow

logger = logging.getLogger(__name__)


class ConsensusWarehouse:
    def __init__(self):
        self.table = "macro_events_consensus"

    async def store(self, event: UniversalMacroEvent) -> bool:
        query = f"""
            INSERT INTO {self.table} (
                event_id, country, currency, title, category, subcategory,
                forecast, previous, actual, consensus, revised_previous,
                importance, impact_score, release_time_utc, status,
                source_url, tags, affected_assets, confidence, quality_score, metadata
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
                      $16, $17, $18, $19, $20, $21)
            ON CONFLICT (event_id, release_time_utc) DO UPDATE SET
                country = EXCLUDED.country,
                currency = EXCLUDED.currency,
                title = EXCLUDED.title,
                category = EXCLUDED.category,
                subcategory = EXCLUDED.subcategory,
                forecast = EXCLUDED.forecast,
                previous = EXCLUDED.previous,
                actual = EXCLUDED.actual,
                consensus = EXCLUDED.consensus,
                revised_previous = EXCLUDED.revised_previous,
                importance = EXCLUDED.importance,
                impact_score = EXCLUDED.impact_score,
                status = EXCLUDED.status,
                source_url = EXCLUDED.source_url,
                tags = EXCLUDED.tags,
                affected_assets = EXCLUDED.affected_assets,
                confidence = EXCLUDED.confidence,
                quality_score = EXCLUDED.quality_score,
                metadata = EXCLUDED.metadata,
                updated_at = NOW()
        """
        try:
            await execute(
                query,
                event.event_id,
                event.country,
                event.currency,
                event.title,
                event.category,
                event.subcategory,
                event.forecast,
                event.previous,
                event.actual,
                event.consensus,
                event.revised_previous,
                event.importance,
                event.impact_score,
                event.release_time_utc,
                event.status,
                event.source_url,
                event.tags,
                event.affected_assets,
                event.confidence,
                event.quality_score,
                json.dumps(event.metadata),
            )
            return True
        except Exception as e:
            logger.error(f"Consensus store error: {e}")
            return False

    # ... rest of the methods unchanged ...
    async def get_today_events(self, country: str = None) -> List[dict]:
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        query = f"SELECT * FROM {self.table} WHERE release_time_utc >= $1 AND release_time_utc < $2"
        params = [today, tomorrow]
        if country:
            query += " AND country = $3"
            params.append(country)
        rows = await fetch(query, *params)
        return [dict(row) for row in rows]

    async def get_upcoming_events(self, hours: int = 48) -> List[dict]:
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)
        query = f"SELECT * FROM {self.table} WHERE release_time_utc >= $1 AND release_time_utc < $2 AND status != 'Released'"
        rows = await fetch(query, now, cutoff)
        return [dict(row) for row in rows]

    async def get_high_impact(self) -> List[dict]:
        query = f"SELECT * FROM {self.table} WHERE importance = 'High' ORDER BY release_time_utc DESC LIMIT 20"
        rows = await fetch(query)
        return [dict(row) for row in rows]

    async def get_event(self, event_id: str) -> Optional[dict]:
        row = await fetchrow(f"SELECT * FROM {self.table} WHERE event_id = $1", event_id)
        return dict(row) if row else None
