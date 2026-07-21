"""
GLB-002 Asset Impact Engine - Schemas
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from .constants import AssetType, Bias
from intelligence.schemas.asset_impact import AssetImpactMatrix


class CurrencyStrength(BaseModel):
    """Individual currency strength analysis"""

    currency: str
    score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)
    factors: Dict[str, float]
    drivers: List[str]
    risks: List[str]


class PairComparison(BaseModel):
    """FX pair comparison result"""

    pair: str
    base_currency: str
    quote_currency: str
    asset_type: AssetType = AssetType.FX

    base_score: float = Field(ge=0, le=100)
    quote_score: float = Field(ge=0, le=100)
    differential: float  # base_score - quote_score

    bias: Bias
    confidence: float = Field(ge=0, le=100)

    drivers: List[Dict[str, Any]]
    risks: List[str]
    evidence: List[Dict[str, Any]]


class AssetImpactReport(BaseModel):
    """GLB-002 Engine Report"""

    engine_id: str = "GLB-002"
    engine_name: str = "Asset Impact Engine"
    version: str = "1.0.0"
    status: str = "OPERATIONAL"
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Individual currency strengths
    currency_strengths: Dict[str, CurrencyStrength]

    # Pair comparisons
    pair_analyses: Dict[str, PairComparison]

    # Asset Impact Matrix (for Global Intelligence Hub)
    asset_impact_matrix: Optional[AssetImpactMatrix] = None

    # Summary
    summary: Dict[str, Any]

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
