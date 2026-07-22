"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Constants
"""

from enum import Enum


class AnalogueQuality(str, Enum):
    """Quality of historical analogue"""

    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    INSUFFICIENT = "INSUFFICIENT"


class TimeHorizon(str, Enum):
    """Time horizons for analysis"""

    INTRADAY = "INTRADAY"
    SHORT_TERM = "SHORT_TERM"  # 1-3 days
    MEDIUM_TERM = "MEDIUM_TERM"  # 5-10 days
    LONG_TERM = "LONG_TERM"  # 20-60 days


class ScenarioType(str, Enum):
    """Scenario types"""

    CONTINUATION = "CONTINUATION"
    REVERSION = "REVERSION"
    NEW_REGIME = "NEW_REGIME"


class AnalogueValidity(str, Enum):
    """Validity of analogue"""

    VALID = "VALID"
    DEGRADING = "DEGRADING"
    INVALID = "INVALID"


# NDIP Topics
NDIP_TOPICS = {
    "HISTORICAL_DATA": "market.historical.data",
    "MARKET_REGIME": "market.regime.snapshot",
    "MACRO_CONDITIONS": "macro.conditions.snapshot",
    "CENTRAL_BANK": "central.bank.policy",
    "GEOPOLITICAL": "geopolitical.risk",
    "CAPITAL_FLOWS": "capital.flows",
    "SENTIMENT": "sentiment.state",
    "POSITIONING": "positioning.state",
    "VOLATILITY": "market.volatility",
}

# Feature weights for similarity calculation
FEATURE_WEIGHTS = {
    "market_regime": 0.15,
    "macro": 0.15,
    "central_banks": 0.12,
    "geopolitical": 0.12,
    "capital_flows": 0.10,
    "sentiment": 0.10,
    "positioning": 0.08,
    "volatility": 0.08,
    "yield_curve": 0.05,
    "liquidity": 0.05,
}

# Time horizons in days
HORIZON_DAYS = {
    TimeHorizon.INTRADAY: 0.04,  # ~1 hour
    TimeHorizon.SHORT_TERM: 3,
    TimeHorizon.MEDIUM_TERM: 10,
    TimeHorizon.LONG_TERM: 30,
}
