"""
GLB-007 Capital Flows & Liquidity Intelligence Engine - Input Schemas
"""

from datetime import datetime

from pydantic import BaseModel, Field

from ..constants import CapitalFlowType, FlowDirection


class CapitalFlowInput(BaseModel):
    """Canonical capital flow input contract"""

    flow_id: str
    asset: str
    region: str
    flow_type: CapitalFlowType
    direction: FlowDirection
    amount: float
    amount_normalized: float = Field(ge=0, le=100)
    velocity: float = Field(ge=0, le=100)
    persistence: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = "NDIP"


class LiquidityInput(BaseModel):
    """Liquidity data input contract"""

    global_liquidity: float = Field(ge=0, le=100)
    central_bank_liquidity: float = Field(ge=0, le=100)
    money_market_liquidity: float = Field(ge=0, le=100)
    credit_liquidity: float = Field(ge=0, le=100)
    funding_stress: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
