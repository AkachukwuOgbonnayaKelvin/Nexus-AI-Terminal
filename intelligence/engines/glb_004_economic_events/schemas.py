"""
GLB-004 Economic Events Engine - Schemas
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from intelligence.schemas.asset_impact import AssetImpactMatrix
from .constants import EventImpact, EventDirection


class EconomicEvent(BaseModel):
    """Single economic event"""

    event: str
    country: str
    currency: str
    impact: EventImpact
    date: datetime
    forecast: float
    previous: float
    actual: Optional[float] = None
    deviation: Optional[float] = None
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
    upcoming_events: List[EconomicEvent]
    recent_events: List[EconomicEvent]

    # Signals, evidence, risks, drivers
    signals: List[EventSignal]
    evidence: List[EventEvidence]
    risks: List[EventRisk]
    drivers: List[EventDriver]

    # Asset Impact Matrix
    asset_impact_matrix: Optional[AssetImpactMatrix] = None

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
