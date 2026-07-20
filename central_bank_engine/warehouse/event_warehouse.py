import json
import logging
from typing import List, Optional

from central_bank_engine.dtos import UniversalCentralBankEvent
from ndip.utils.db_connector import execute, fetch, fetchrow

logger = logging.getLogger(__name__)


class CentralBankWarehouse:
    def __init__(self):
        self.table = "central_bank_events"

    async def store(self, event: UniversalCentralBankEvent) -> bool:
        query = f"""
            INSERT INTO {self.table} (
                event_id, provider, bank, country, currency, event_type,
                title, summary, statement, release_time, meeting_date, effective_date,
                old_rate, new_rate, rate_change, vote_split, governor,
                importance, policy_bias, hawkish_dovish_score, communication_type,
                source_url, attachments, document_hash, confidence, metadata
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
                      $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26)
            ON CONFLICT (event_id) DO UPDATE SET
                title = EXCLUDED.title,
                summary = EXCLUDED.summary,
                statement = EXCLUDED.statement,
                release_time = EXCLUDED.release_time,
                meeting_date = EXCLUDED.meeting_date,
                effective_date = EXCLUDED.effective_date,
                old_rate = EXCLUDED.old_rate,
                new_rate = EXCLUDED.new_rate,
                rate_change = EXCLUDED.rate_change,
                vote_split = EXCLUDED.vote_split,
                governor = EXCLUDED.governor,
                importance = EXCLUDED.importance,
                policy_bias = EXCLUDED.policy_bias,
                hawkish_dovish_score = EXCLUDED.hawkish_dovish_score,
                communication_type = EXCLUDED.communication_type,
                source_url = EXCLUDED.source_url,
                attachments = EXCLUDED.attachments,
                document_hash = EXCLUDED.document_hash,
                confidence = EXCLUDED.confidence,
                metadata = EXCLUDED.metadata
        """
        try:
            await execute(
                query,
                event.event_id,
                event.provider,
                event.bank,
                event.country,
                event.currency,
                event.event_type,
                event.title,
                event.summary,
                event.statement,
                event.release_time,
                event.meeting_date,
                event.effective_date,
                event.old_rate,
                event.new_rate,
                event.rate_change,
                event.vote_split,
                event.governor,
                event.importance,
                event.policy_bias,
                event.hawkish_dovish_score,
                event.communication_type,
                event.source_url,
                event.attachments,
                event.document_hash,
                event.confidence,
                json.dumps(event.metadata),
            )
            return True
        except Exception as e:
            logger.error(f"Central Bank store error: {e}")
            return False

    async def get_latest_rate(self, bank: str = "Federal Reserve") -> Optional[dict]:
        query = f"""
            SELECT * FROM {self.table}
            WHERE bank = $1 AND event_type = 'RateDecision'
            ORDER BY release_time DESC LIMIT 1
        """
        row = await fetchrow(query, bank)
        return dict(row) if row else None

    async def get_latest_statement(
        self, bank: str = "Federal Reserve"
    ) -> Optional[dict]:
        query = f"""
            SELECT * FROM {self.table}
            WHERE bank = $1 AND event_type IN ('Statement', 'Minutes')
            ORDER BY release_time DESC LIMIT 1
        """
        row = await fetchrow(query, bank)
        return dict(row) if row else None

    async def get_meeting_calendar(self, bank: str = "Federal Reserve") -> List[dict]:
        query = f"""
            SELECT * FROM {self.table}
            WHERE bank = $1 AND event_type = 'MeetingCalendar'
            ORDER BY release_time DESC
        """
        rows = await fetch(query, bank)
        return [dict(row) for row in rows]

    async def get_latest(self, limit: int = 20) -> List[dict]:
        query = f"SELECT * FROM {self.table} ORDER BY release_time DESC LIMIT $1"
        rows = await fetch(query, limit)
        return [dict(row) for row in rows]

    async def get_by_importance(self, importance: str, limit: int = 20) -> List[dict]:
        query = f"""
            SELECT * FROM {self.table}
            WHERE importance = $1
            ORDER BY release_time DESC LIMIT $2
        """
        rows = await fetch(query, importance, limit)
        return [dict(row) for row in rows]
