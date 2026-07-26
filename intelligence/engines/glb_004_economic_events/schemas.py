"""
GLB-004 Economic Events Engine - Schemas
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from intelligence.schemas.asset_impact import AssetImpactMatrix

from .constants import EventDirection, EventImpact


class EconomicEvent(BaseModel):
    """Single economic event"""

    event: str
    country: str
    currency: str
    impact: EventImpact
    date: datetime
    forecast: float
    previous: float
    actual: float | None = None
    deviation: float | None = None
    volatility_forecast: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)


class EventSignal(BaseModel):
    """Signal from event analysis"""

    name: str
    direction: EventDirection
    weight: float = Field(ge=0, le=1)


class EventEvidence(BaseModel):
    """Evidence for event analysis"""

    source: str
    indicator: str
    value: Any
    contribution: float = Field(ge=0, le=1)


class EventRisk(BaseModel):
    """Risk from events"""

    description: str
    probability: float = Field(ge=0, le=1)
    impact: str


class EventDriver(BaseModel):
    """Driver from events"""

    name: str
    direction: EventDirection
    strength: float = Field(ge=0, le=1)


class EventsReport(BaseModel):
    """GLB-004 Engine Report"""

    engine_id: str = "GLB-004"
    engine_name: str = "Economic Events Engine"
    version: str = "1.0.0"
    status: str = "OPERATIONAL"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Core intelligence
    total_events: int
    high_impact_events: int
    medium_impact_events: int
    low_impact_events: int
    overall_volatility_forecast: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)

    # Events
    upcoming_events: list[EconomicEvent]
    recent_events: list[EconomicEvent]

    # Signals, evidence, risks, drivers
    signals: list[EventSignal]
    evidence: list[EventEvidence]
    risks: list[EventRisk]
    drivers: list[EventDriver]

    # Asset Impact Matrix
    asset_impact_matrix: AssetImpactMatrix | None = None

    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict)
