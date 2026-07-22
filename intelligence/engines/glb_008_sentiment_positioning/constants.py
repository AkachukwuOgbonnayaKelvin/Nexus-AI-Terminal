"""
GLB-008 Sentiment & Positioning Intelligence Engine - Constants
"""

from enum import Enum


class SentimentState(str, Enum):
    """Global sentiment state"""

    RISK_ON = "RISK_ON"
    RISK_OFF = "RISK_OFF"
    NEUTRAL = "NEUTRAL"
    EXTREME = "EXTREME"
    DIVERGENT = "DIVERGENT"


class PositioningBias(str, Enum):
    """Positioning bias"""

    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"
    EXTREME_LONG = "EXTREME_LONG"
    EXTREME_SHORT = "EXTREME_SHORT"


class CrowdingState(str, Enum):
    """Crowding state"""

    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class SentimentType(str, Enum):
    """Type of sentiment"""

    RETAIL = "RETAIL"
    INSTITUTIONAL = "INSTITUTIONAL"
    COT = "COT"
    OPTIONS = "OPTIONS"
    FUTURES = "FUTURES"


# NDIP Topics
NDIP_TOPICS = {
    "COT_DATA": "positioning.cot",
    "RETAIL_SENTIMENT": "sentiment.retail",
    "INSTITUTIONAL_POSITIONING": "positioning.institutional",
    "OPTIONS_DATA": "options.sentiment",
    "FUTURES_DATA": "futures.positioning",
    "RISK_APPETITE": "sentiment.risk_appetite",
}

# Asset exposure to sentiment
ASSET_SENTIMENT_EXPOSURE = {
    # Risk-on assets (positive with bullish sentiment)
    "US500": 0.85,
    "US100": 0.90,
    "US30": 0.80,
    "GER40": 0.80,
    "UK100": 0.75,
    "JP225": 0.70,
    "AUDUSD": 0.80,
    "NZDUSD": 0.75,
    "EURUSD": 0.60,
    "GBPUSD": 0.55,
    # Safe havens (negative with risk-on sentiment)
    "USDJPY": -0.70,
    "USDCHF": -0.80,
    "XAUUSD": -0.65,
    # Commodities (positive with risk-on)
    "WTI": 0.70,
    "BRENT": 0.70,
    "XAGUSD": 0.60,
}

# Sentiment extremes thresholds
EXTREME_THRESHOLDS = {
    "percentile_high": 85.0,
    "percentile_low": 15.0,
    "crowding_high": 80.0,
    "sentiment_high": 80.0,
    "sentiment_low": 20.0,
}
