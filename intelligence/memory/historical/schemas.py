"""
Historical Memory - Canonical Schemas

This defines the global time-indexed format for historical memory.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class MarketState(BaseModel):
    """Market state at a specific point in time"""

    regime: str = "NEUTRAL"
    macro_score: float = 50.0
    central_bank_score: float = 50.0
    geopolitical_risk: float = 50.0
    capital_flow_score: float = 50.0
    sentiment_score: float = 50.0
    positioning_score: float = 50.0
    volatility_score: float = 50.0


class AssetPrice(BaseModel):
    """Price data for a single asset at a point in time"""

    close: float
    open: float | None = None
    high: float | None = None
    low: float | None = None


class ForwardReturn(BaseModel):
    """Forward return for a specific horizon"""

    return_pct: float
    direction: str = "NEUTRAL"  # BULLISH, BEARISH, NEUTRAL
    win: bool = False
    confidence: float = 70.0


class AssetOutcome(BaseModel):
    """Outcome for a single asset from a historical window"""

    symbol: str
    price: AssetPrice
    forward_returns: dict[str, ForwardReturn]  # horizon -> ForwardReturn


class HistoricalWindow(BaseModel):
    """Canonical global historical window"""

    window_id: str
    timestamp: datetime

    # Market state
    market_state: MarketState

    # All assets at this timestamp
    assets: dict[str, AssetOutcome]

    # Coverage metrics
    total_assets: int
    available_assets: int
    coverage_ratio: float = Field(ge=0, le=1)

    # Validation
    is_valid: bool = True
    rejection_reason: str | None = None

    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict)
