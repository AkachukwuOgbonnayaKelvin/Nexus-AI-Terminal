"""
GLB-006 Geopolitical Risk Intelligence Engine - Input Schemas
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from ..constants import GeopoliticalEventType


class GeopoliticalEventInput(BaseModel):
    """Canonical geopolitical event input contract"""

    event_id: str
    event_type: GeopoliticalEventType
    headline: str
    description: Optional[str] = None

    # Geography
    countries: List[str]
    region: str

    # Risk metrics
    severity: float = Field(ge=0, le=100)
    escalation_probability: float = Field(ge=0, le=100)
    strategic_importance: float = Field(ge=0, le=100)
    economic_exposure: float = Field(ge=0, le=100)
    market_sensitivity: float = Field(ge=0, le=100)

    # Metadata
    timestamp: datetime
    source: str
    confidence: float = Field(ge=0, le=100)

    # Additional context
    context: Optional[Dict[str, Any]] = None
