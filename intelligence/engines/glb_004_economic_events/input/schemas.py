"""
GLB-004 Economic Events Intelligence Engine - Input Schemas
"""

from datetime import datetime

from pydantic import BaseModel

from ..constants import EventCategory, EventImpact, EventStatus


class EconomicEventInput(BaseModel):
    """Canonical economic event input contract"""

    event_id: str

    event_name: str
    country: str
    currency: str

    scheduled_at: datetime

    impact_level: EventImpact

    category: EventCategory

    previous: float | None = None
    forecast: float | None = None
    actual: float | None = None

    unit: str | None = None

    revision: float | None = None

    source: str

    status: EventStatus = EventStatus.UPCOMING
