"""
GLB-001 Market Regime Engine - Constants & Enums
"""

from enum import Enum


class MarketRegime(str, Enum):
    """Primary market regime classifications"""

    RISK_ON = "RISK_ON"
    RISK_OFF = "RISK_OFF"
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    TRANSITION = "TRANSITION"
    VOLATILE = "VOLATILE"


class TransitionState(str, Enum):
    """Transition state between regimes"""

    STABLE = "STABLE"
    WEAKENING = "WEAKENING"
    STRENGTHENING = "STRENGTHENING"
    REVERSING = "REVERSING"


class RegimeAlignment(str, Enum):
    """How regime aligns with an asset"""

    STRONGLY_SUPPORTIVE = "STRONGLY_SUPPORTIVE"
    SUPPORTIVE = "SUPPORTIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    STRONGLY_NEGATIVE = "STRONGLY_NEGATIVE"
    MIXED = "MIXED"


# NDIP Topics
NDIP_TOPICS = {
    "PRICE_SNAPSHOT": "market.price.snapshot",
    "TREND_SNAPSHOT": "market.trend.snapshot",
    "VOLATILITY_SNAPSHOT": "market.volatility.snapshot",
    "BREADTH_SNAPSHOT": "market.breadth.snapshot",
    "RISK_SNAPSHOT": "market.risk.snapshot",
    "MACRO_CONDITIONS": "macro.conditions.snapshot",
    "MACRO_GROWTH": "macro.growth.snapshot",
    "MACRO_INFLATION": "macro.inflation.snapshot",
}

# Default dimension weights
DIMENSION_WEIGHTS = {
    "risk_sentiment": 0.25,
    "trend_strength": 0.20,
    "volatility": 0.15,
    "momentum": 0.10,
    "breadth": 0.10,
    "macro_growth": 0.10,
    "inflation_pressure": 0.05,
    "liquidity": 0.05,
}

# Assets that GLB-001 provides context for
SUPPORTED_ASSETS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "NZDUSD",
    "USDCAD",
    "USDCHF",
    "XAUUSD",
    "XAGUSD",
    "US500",
    "US100",
    "US30",
    "GER40",
    "UK100",
    "JP225",
    "HK50",
    "AU200",
]
