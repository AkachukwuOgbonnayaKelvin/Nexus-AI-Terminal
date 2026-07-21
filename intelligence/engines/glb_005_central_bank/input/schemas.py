"""
GLB-005 Central Bank Intelligence Engine - Input Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from ..constants import CentralBank, PolicyStance, BalanceSheetPolicy


class RateExpectation(BaseModel):
    """Rate expectations over time"""

    current: float
    three_month: float
    six_month: float
    twelve_month: float
    confidence: float = Field(ge=0, le=100)


class BalanceSheetData(BaseModel):
    """Balance sheet policy data"""

    policy: BalanceSheetPolicy
    size: float  # In trillions
    monthly_change: float
    direction: str  # EXPANDING, CONTRACTING, STABLE


class CentralBankInput(BaseModel):
    """Canonical central bank input contract"""

    bank: CentralBank
    currency: str

    # Policy stance
    policy_stance: PolicyStance
    policy_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)

    # Current rate
    current_rate: float

    # Rate expectations
    rate_expectations: RateExpectation

    # Forward guidance
    forward_guidance_tone: PolicyStance
    forward_guidance_score: float = Field(ge=0, le=100)

    # Balance sheet
    balance_sheet: Optional[BalanceSheetData] = None

    # Next meeting
    next_meeting: Optional[datetime] = None
    expected_change: Optional[float] = None

    # Source
    source: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
