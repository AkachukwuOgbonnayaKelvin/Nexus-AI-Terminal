"""
Canonical Asset Impact Contract - v1.0 (FROZEN)

This contract is now locked. No new fields may be added without version bump.
All Global Intelligence engines must adhere to this exact schema.

Version: 1.0.0
Status: FROZEN
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum


class AssetType(str, Enum):
    FX = "FX"
    COMMODITY = "COMMODITY"
    EQUITY = "EQUITY"
    BOND = "BOND"
    CRYPTO = "CRYPTO"


class Direction(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class ImpactStatus(str, Enum):
    ANALYZED = "ANALYZED"
    NOT_COVERED = "NOT_COVERED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ImpactDriver(BaseModel):
    """Driver of the impact - v1.0"""

    name: str
    direction: Direction
    strength: float = Field(ge=0, le=1)

    # Optional: Which engine specific factor drove this
    factor: Optional[str] = None


class AssetImpact(BaseModel):
    """
    Canonical Asset Impact - v1.0 (FROZEN)

    All engines must produce this for each asset.
    Internal score: -100 to +100 (signed)
    """

    asset: str
    asset_type: AssetType

    # Signed directional score: -100 to +100
    # +100 = strongly bullish, 0 = neutral, -100 = strongly bearish
    score: float = Field(ge=-100, le=100)

    direction: Direction
    confidence: float = Field(ge=0, le=100)
    status: ImpactStatus = ImpactStatus.ANALYZED

    # Drivers explaining the impact
    drivers: List[ImpactDriver] = Field(default_factory=list)

    # Relevance of this engine to this asset (0.0 = not relevant, 1.0 = highly relevant)
    relevance: float = Field(ge=0, le=1, default=0.5)

    # Engine metadata
    engine_id: str
    engine_name: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"

    @field_validator("score")
    @classmethod
    def validate_score(cls, v: float) -> float:
        """Ensure score is within -100 to +100"""
        if v < -100 or v > 100:
            raise ValueError(f"Score must be between -100 and 100, got {v}")
        return v

    def to_display_score(self) -> float:
        """Convert -100 to +100 to 0-100 display score"""
        return 50 + (self.score / 2)


class AssetImpactMatrix(BaseModel):
    """
    Standard output from every Global Intelligence sub-engine - v1.0 (FROZEN)

    Contains canonical AssetImpact objects.
    """

    engine_id: str
    engine_name: str
    version: str = "1.0.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Map of asset → AssetImpact
    impacts: dict[str, AssetImpact]

    # Which assets does this engine understand well?
    covered_assets: List[str]

    # Overall confidence of this engine's asset impacts
    overall_confidence: float = Field(ge=0, le=100)

    # Metadata about this engine's analysis
    metadata: dict = Field(default_factory=dict)

    def get_impact(self, asset: str) -> Optional[AssetImpact]:
        """Get impact for a specific asset."""
        return self.impacts.get(asset)

    def get_display_score(self, asset: str) -> float:
        """Get 0-100 display score for an asset."""
        impact = self.get_impact(asset)
        if impact is None:
            return 50.0
        return impact.to_display_score()

    def get_direction(self, asset: str) -> str:
        """Get direction for an asset."""
        impact = self.get_impact(asset)
        if impact is None:
            return "NEUTRAL"
        return impact.direction.value

    def get_status(self, asset: str) -> str:
        """Get status for an asset."""
        impact = self.get_impact(asset)
        if impact is None:
            return ImpactStatus.NOT_COVERED.value
        return impact.status.value
