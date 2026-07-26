from datetime import datetime
from typing import Any

from macroeconomic_events_engine.dtos import UniversalMacroEvent


class InvestingAdapter:
    def adapt(self, raw: dict[str, Any], provider_name: str) -> UniversalMacroEvent:
        release_time = raw.get("release_time_utc")
        if isinstance(release_time, str):
            release_time = datetime.fromisoformat(release_time)
        return UniversalMacroEvent(
            event_id=raw.get("event_id", "inv_unknown"),
            provider=provider_name,
            provider_event_id=raw.get("event_id", ""),
            country=raw.get("country", "US"),
            currency=raw.get("currency", "USD"),
            title=raw.get("title", "Unknown"),
            category=raw.get("category", "Unknown"),
            forecast=raw.get("forecast"),
            previous=raw.get("previous"),
            actual=raw.get("actual"),
            importance=raw.get("importance", "Medium"),
            release_time_utc=release_time or datetime.now(),
            status=raw.get("status", "Scheduled"),
            confidence=0.65,
            quality_score=0.65,
            metadata=raw,
        )
