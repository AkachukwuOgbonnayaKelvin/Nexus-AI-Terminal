"""
GLB-003 Macro Intelligence Engine - Schemas
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from intelligence.schemas.asset_impact import AssetImpactMatrix


class MacroComponent(BaseModel):
    """Single macro component analysis"""

    name: str
    score: float = Field(ge=0, le=100)
    value: float
    trend: str
    signal: str
    confidence: float = Field(ge=0, le=100)


class MacroSignal(BaseModel):
    """Macro intelligence signal"""

    name: str
    value: str
    weight: float = Field(ge=0, le=1)


class MacroEvidence(BaseModel):
    """Evidence for macro analysis"""

    source: str
    indicator: str
    value: Any
    contribution: float = Field(ge=0, le=1)


class MacroRisk(BaseModel):
    """Macro risk"""

    description: str
    probability: float = Field(ge=0, le=1)
    impact: str


class MacroDriver(BaseModel):
    """Macro driver"""

    name: str
    direction: str
    strength: float = Field(ge=0, le=1)


class MacroReport(BaseModel):
    """GLB-003 Engine Report"""

    engine_id: str = "GLB-003"
    engine_name: str = "Macro Intelligence Engine"
    version: str = "1.0.0"
    status: str = "OPERATIONAL"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    overall_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)

    macro_components: dict[str, MacroComponent]
    signals: list[MacroSignal]
    evidence: list[MacroEvidence]
    risks: list[MacroRisk]
    drivers: list[MacroDriver]

    asset_impact_matrix: AssetImpactMatrix | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
