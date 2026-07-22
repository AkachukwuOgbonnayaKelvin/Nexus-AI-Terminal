"""
GLB-008 Sentiment & Positioning Intelligence Engine - Input Schemas
"""

from datetime import datetime
from pydantic import BaseModel, Field

from ..constants import PositioningBias


class COTInput(BaseModel):
    """Commitment of Traders input"""

    symbol: str
    report_date: datetime
    dealer_long: float
    dealer_short: float
    asset_manager_long: float
    asset_manager_short: float
    leveraged_funds_long: float
    leveraged_funds_short: float
    net_position: float
    percentile: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)


class RetailSentimentInput(BaseModel):
    """Retail sentiment input"""

    symbol: str
    bullish_percent: float = Field(ge=0, le=100)
    bearish_percent: float = Field(ge=0, le=100)
    neutral_percent: float = Field(ge=0, le=100)
    net_sentiment: float = Field(ge=-100, le=100)
    confidence: float = Field(ge=0, le=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class InstitutionalPositioningInput(BaseModel):
    """Institutional positioning input"""

    asset: str
    net_position: float
    positioning_bias: PositioningBias
    percentile: float = Field(ge=0, le=100)
    crowding: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class OptionsSentimentInput(BaseModel):
    """Options sentiment input"""

    symbol: str
    put_call_ratio: float
    implied_volatility: float
    skew: float
    sentiment_score: float = Field(ge=-100, le=100)
    confidence: float = Field(ge=0, le=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
