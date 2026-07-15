"""Universal Intelligence Standard Schemas.

This module defines the required output structure for all intelligence engines.
"""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ConfidenceScore(BaseModel):
    """Confidence scoring structure."""

    model_config = ConfigDict(extra="ignore")

    score: float = Field(
        ..., ge=0, le=1, description="Confidence score between 0 and 1"
    )
    calibration: Optional[float] = Field(None, description="Calibration metric")
    factors: List[str] = Field(
        default_factory=list, description="Factors influencing confidence"
    )


class EvidenceItem(BaseModel):
    """Individual evidence item."""

    model_config = ConfigDict(extra="ignore")

    type: str = Field(
        ...,
        description="Type of evidence (e.g., 'technical', 'macro', 'institutional')",
    )
    source: str = Field(..., description="Source of evidence")
    description: str = Field(..., description="Human-readable description")
    weight: float = Field(1.0, ge=0, le=1, description="Weight of this evidence")
    timestamp: datetime = Field(default_factory=datetime.now)


class RiskAssessment(BaseModel):
    """Risk assessment structure."""

    model_config = ConfigDict(extra="ignore")

    level: str = Field(..., description="Risk level: 'Low', 'Medium', 'High'")
    factors: List[str] = Field(default_factory=list, description="Risk factors")
    mitigation: List[str] = Field(
        default_factory=list, description="Mitigation strategies"
    )


class Recommendation(BaseModel):
    """Recommendation structure."""

    model_config = ConfigDict(extra="ignore")

    action: str = Field(..., description="Recommended action")
    rationale: str = Field(..., description="Rationale for recommendation")
    confidence: float = Field(
        ..., ge=0, le=1, description="Confidence in recommendation"
    )


class IntelligenceMetadata(BaseModel):
    """Metadata for intelligence output."""

    model_config = ConfigDict(extra="ignore")

    engine: str = Field(..., description="Engine that generated this intelligence")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(..., description="Version of the engine")
    sources: List[str] = Field(default_factory=list, description="Data sources used")
    processing_time_ms: Optional[float] = Field(
        None, description="Processing time in milliseconds"
    )


class IntelligenceHealth(BaseModel):
    """Health status of the intelligence engine."""

    model_config = ConfigDict(extra="ignore")

    status: str = Field(
        ..., description="Health status: 'Healthy', 'Degraded', 'Unhealthy'"
    )
    last_run: datetime = Field(default_factory=datetime.now)
    data_freshness: float = Field(..., description="Age of data in seconds")
    errors: List[str] = Field(default_factory=list, description="Recent errors")


class UniversalIntelligence(BaseModel):
    """Universal Intelligence Standard - Required output for all engines."""

    model_config = ConfigDict(extra="ignore")

    executive_summary: str = Field(..., description="Human-readable executive summary")
    executive_ai_summary: str = Field(..., description="AI-generated executive summary")
    confidence: ConfidenceScore = Field(..., description="Confidence scoring")
    evidence: Dict[str, List[EvidenceItem]] = Field(
        default_factory=lambda: {"supporting": [], "contradicting": []},
        description="Supporting and contradicting evidence",
    )
    risk: RiskAssessment = Field(..., description="Risk assessment")
    recommendations: List[Recommendation] = Field(default_factory=list)
    metadata: IntelligenceMetadata = Field(..., description="Metadata")
    health: IntelligenceHealth = Field(..., description="Engine health")
