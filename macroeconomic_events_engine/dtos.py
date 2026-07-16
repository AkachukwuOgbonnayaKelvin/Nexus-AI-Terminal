"""Universal Macro Event DTO – used across all providers and layers."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UniversalMacroEvent(BaseModel):
    event_id: str
    provider: str
    provider_event_id: str
    country: str
    currency: str
    title: str
    category: str
    subcategory: Optional[str] = None
    forecast: Optional[float] = None
    previous: Optional[float] = None
    actual: Optional[float] = None
    consensus: Optional[float] = None
    revised_previous: Optional[float] = None
    importance: str  # High, Medium, Low
    impact_score: int = 50  # 0-100
    release_time_utc: datetime
    release_time_local: Optional[datetime] = None
    timezone: str = "UTC"
    status: str  # Scheduled, Forecast, Consensus, Released, Revised, Archived
    source_url: Optional[str] = None
    tags: List[str] = []
    affected_assets: List[str] = []
    confidence: float = 1.0
    quality_score: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
