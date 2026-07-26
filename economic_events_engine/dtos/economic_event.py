from datetime import datetime

from pydantic import BaseModel


class UniversalEconomicEvent(BaseModel):
    event_id: str
    provider: str
    provider_event_id: str
    country: str
    region: str | None = None
    currency: str
    title: str
    short_title: str
    category: str
    subcategory: str | None = None
    forecast: float | None = None
    previous: float | None = None
    actual: float | None = None
    consensus: float | None = None
    revised_previous: float | None = None
    importance: str  # High, Medium, Low
    release_time_utc: datetime
    release_time_local: datetime | None = None
    timezone: str
    frequency: str
    status: str
    source_url: str | None = None
    tags: list[str] = []
    affected_assets: list[str] = []
    affected_markets: list[str] = []
    confidence: float = 1.0
    quality_score: float = 1.0
    metadata: dict = {}
