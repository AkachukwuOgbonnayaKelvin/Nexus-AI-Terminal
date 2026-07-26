"""Normalizer – converts to UniversalCentralBankEvent."""

import logging
from typing import Any

from central_bank_engine.dtos import UniversalCentralBankEvent

logger = logging.getLogger(__name__)


class Normalizer:
    def normalize(
        self, events: list[dict[str, Any]]
    ) -> list[UniversalCentralBankEvent]:
        normalized = []
        for event in events:
            try:
                # Convert to DTO
                dto = UniversalCentralBankEvent(
                    event_id=event.get("event_id"),
                    provider=event.get("provider", "central_bank"),
                    bank=event.get("bank"),
                    country=event.get("country"),
                    currency=event.get("currency"),
                    event_type=event.get("event_type"),
                    title=event.get("title"),
                    summary=event.get("summary"),
                    statement=event.get("statement"),
                    release_time=event.get("release_time"),
                    meeting_date=event.get("meeting_date"),
                    effective_date=event.get("effective_date"),
                    old_rate=event.get("old_rate"),
                    new_rate=event.get("rate"),
                    rate_change=event.get("rate_change"),
                    vote_split=event.get("vote_split"),
                    governor=event.get("governor"),
                    importance=event.get("importance", "Medium"),
                    policy_bias=event.get("policy_bias"),
                    communication_type=event.get("communication_type", "Statement"),
                    source_url=event.get("source_url"),
                    attachments=event.get("attachments", []),
                    document_hash=event.get("document_hash"),
                    confidence=event.get("confidence", 0.8),
                    metadata=event.get("metadata", {}),
                )
                normalized.append(dto)
            except Exception as e:
                logger.error(
                    f"Normalization failed: {e} for event {event.get('event_id')}"
                )
        logger.info(f"Normalized {len(normalized)} events")
        return normalized
