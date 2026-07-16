from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UniversalEconomicEvent(BaseModel):
    event_id: str
    provider: str
    provider_event_id: str
    country: str
    region: Optional[str] = None
    currency: str
    title: str
    short_title: str
    category: str
    subcategory: Optional[str] = None
    forecast: Optional[float] = None
    previous: Optional[float] = None
    actual: Optional[float] = None
    consensus: Optional[float] = None
    revised_previous: Optional[float] = None
    importance: str  # High, Medium, Low
    release_time_utc: datetime
    release_time_local: Optional[datetime] = None
    timezone: str
    frequency: str
    status: str
    source_url: Optional[str] = None
    tags: List[str] = []
    affected_assets: List[str] = []
    affected_markets: List[str] = []
    confidence: float = 1.0
    quality_score: float = 1.0
    metadata: dict = {}
