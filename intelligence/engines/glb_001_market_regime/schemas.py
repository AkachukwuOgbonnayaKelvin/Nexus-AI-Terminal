"""
GLB-001 Market Regime Engine - Pydantic Schemas
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from intelligence.schemas.asset_impact import AssetImpactMatrix

from .constants import MarketRegime, RegimeAlignment, TransitionState

# Standard direction types for the Universal Intelligence Contract
Direction = Literal["BULLISH", "BEARISH", "NEUTRAL"]


class MarketDimension(BaseModel):
    """Single market dimension score"""

    name: str
    value: float = Field(ge=0, le=100)
    weight: float = Field(ge=0, le=1)
    contribution: float
    direction: Direction


class RegimeSignal(BaseModel):
    """Intelligence signal from regime analysis"""

    name: str
    value: str
    weight: float = Field(ge=0, le=1)
    contribution: float


class RegimeEvidence(BaseModel):
    """Evidence supporting regime classification"""

    source: str
    indicator: str
    value: Any
    contribution: float = Field(ge=0, le=1)
    direction: Direction


class RegimeRisk(BaseModel):
    """Risk identified in current regime"""

    description: str
    probability: float = Field(ge=0, le=1)
    impact: str
    time_horizon: str


class RegimeDriver(BaseModel):
    """Driver of current regime"""

    name: str
    direction: Direction
    strength: float = Field(ge=0, le=1)


class AssetRegimeContext(BaseModel):
    """Regime context for a specific asset"""

    asset: str
    regime_alignment: RegimeAlignment
    regime_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)
    primary_factor: str


class RegimeReport(BaseModel):
    """GLB-001 Engine Report (Universal Contract)"""

    engine_id: str = "GLB-001"
    engine_name: str = "Market Regime Engine"
    version: str = "1.0.0"
    status: str = "OPERATIONAL"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    primary_regime: MarketRegime
    secondary_regime: MarketRegime | None = None
    transition_state: TransitionState = TransitionState.STABLE

    regime_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)

    dimensions: list[MarketDimension]
    regime_probabilities: dict[str, float]
    signals: list[RegimeSignal]
    evidence: list[RegimeEvidence]
    risks: list[RegimeRisk]
    drivers: list[RegimeDriver]

    asset_context: dict[str, AssetRegimeContext]

    # Asset Impact Matrix (for Global Intelligence Hub)
    asset_impact_matrix: AssetImpactMatrix | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
