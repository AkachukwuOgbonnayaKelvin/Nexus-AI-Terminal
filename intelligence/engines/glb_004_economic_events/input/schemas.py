"""
GLB-004 Economic Events Intelligence Engine - Input Schemas
"""

from datetime import datetime
from typing import Optional
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

    previous: Optional[float] = None
    forecast: Optional[float] = None
    actual: Optional[float] = None

    unit: Optional[str] = None

    revision: Optional[float] = None

    source: str

    status: EventStatus = EventStatus.UPCOMING
