"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Input Schemas
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class MarketSnapshot(BaseModel):
    """Current market snapshot for similarity matching"""

    timestamp: datetime
    regime: str = "NEUTRAL"
    macro_score: float = 50.0
    central_bank_score: float = 50.0
    geopolitical_risk: float = 50.0
    capital_flow_score: float = 50.0
    sentiment_score: float = 50.0
    positioning_score: float = 50.0
    volatility_score: float = 50.0
    asset_prices: Dict[str, float] = Field(default_factory=dict)


class AssetPriceSeries(BaseModel):
    """Historical price series for a single asset"""

    close: List[float] = Field(default_factory=list)
    open: Optional[List[float]] = None
    high: Optional[List[float]] = None
    low: Optional[List[float]] = None


class ForwardReturn(BaseModel):
    """Forward return for a specific horizon"""

    return_pct: float
    direction: str = "NEUTRAL"  # BULLISH, BEARISH, NEUTRAL
    win: bool = False
    confidence: float = 70.0


class EnvironmentState(BaseModel):
    """Current environment state for similarity matching"""

    regime: str = "NEUTRAL"
    macro_score: float = 50.0
    central_bank_score: float = 50.0
    geopolitical_risk: float = 50.0
    capital_flow_score: float = 50.0
    sentiment_score: float = 50.0
    positioning_score: float = 50.0
    volatility_score: float = 50.0


class HistoricalWindow(BaseModel):
    """Complete historical window for analogue comparison"""

    window_id: str
    timestamp: datetime

    # Environment state
    environment: EnvironmentState

    # Asset price series
    asset_prices: Dict[str, AssetPriceSeries]

    # Forward returns by horizon
    forward_returns: Dict[str, ForwardReturn]

    # Metadata
    symbol: str = ""
    window_size: int = 30
    similarity_score: float = 0.0
    quality_score: float = 0.0
