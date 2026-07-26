from datetime import datetime
from typing import Any

from macroeconomic_events_engine.dtos import UniversalMacroEvent


class TradingEconomicsAdapter:
    def adapt(self, raw: dict[str, Any], provider_name: str) -> UniversalMacroEvent:
        release_time = raw.get("DateTime")
        if isinstance(release_time, str):
            release_time = datetime.fromisoformat(release_time.replace("Z", "+00:00"))
        return UniversalMacroEvent(
            event_id=f"te_{raw.get('CalendarId', raw.get('EventId', 'unknown'))}_{raw.get('Country', 'US')}",
            provider=provider_name,
            provider_event_id=str(raw.get("CalendarId", raw.get("EventId", ""))),
            country=raw.get("Country", "US"),
            currency=raw.get("Currency", "USD"),
            title=raw.get("Title", raw.get("Event", "Unknown")),
            category=raw.get("Category", "Unknown"),
            subcategory=raw.get("Subcategory"),
            forecast=raw.get("Forecast"),
            previous=raw.get("Previous"),
            actual=raw.get("Actual"),
            consensus=None,
            revised_previous=raw.get("RevisedPrevious"),
            importance=raw.get("Importance", "Medium"),
            impact_score=0,
            release_time_utc=release_time or datetime.now(),
            timezone=raw.get("TimeZone", "UTC"),
            status="Scheduled" if raw.get("Actual") is None else "Released",
            source_url=raw.get("Url"),
            tags=[raw.get("Category", "Unknown")],
            affected_assets=[],
            confidence=0.9,
            quality_score=0.9,
            metadata=raw,
        )
