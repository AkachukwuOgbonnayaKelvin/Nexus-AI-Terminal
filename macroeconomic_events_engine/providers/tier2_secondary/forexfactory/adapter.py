from datetime import datetime
from typing import Any, Dict

from macroeconomic_events_engine.dtos import UniversalMacroEvent


class ForexFactoryAdapter:
    def adapt(self, raw: Dict[str, Any], provider_name: str) -> UniversalMacroEvent:
        release_time = raw.get("release_time_utc")
        if isinstance(release_time, str):
            release_time = datetime.fromisoformat(release_time)
        return UniversalMacroEvent(
            event_id=raw.get("event_id", "ff_unknown"),
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
            confidence=0.7,
            quality_score=0.7,
            metadata=raw,
        )
