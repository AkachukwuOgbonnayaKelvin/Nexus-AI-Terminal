"""Universal Macro Event DTO – used across all providers and layers."""

from datetime import datetime

from pydantic import BaseModel


class UniversalMacroEvent(BaseModel):
    event_id: str
    provider: str
    provider_event_id: str
    country: str
    currency: str
    title: str
    category: str
    subcategory: str | None = None
    forecast: float | None = None
    previous: float | None = None
    actual: float | None = None
    consensus: float | None = None
    revised_previous: float | None = None
    importance: str  # High, Medium, Low
    impact_score: int = 50  # 0-100
    release_time_utc: datetime
    release_time_local: datetime | None = None
    timezone: str = "UTC"
    status: str  # Scheduled, Forecast, Consensus, Released, Revised, Archived
    source_url: str | None = None
    tags: list[str] = []
    affected_assets: list[str] = []
    confidence: float = 1.0
    quality_score: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
