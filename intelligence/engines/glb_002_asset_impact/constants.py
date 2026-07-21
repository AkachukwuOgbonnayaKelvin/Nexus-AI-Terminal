"""
GLB-002 Asset Impact Engine - Constants
"""

from enum import Enum


class AssetType(str, Enum):
    """Types of assets"""

    FX = "FX"
    COMMODITY = "COMMODITY"
    EQUITY = "EQUITY"
    BOND = "BOND"
    CRYPTO = "CRYPTO"


class Bias(str, Enum):
    """Directional bias"""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


# Currencies supported
CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "JPY",
    "CHF",
    "CAD",
    "AUD",
    "NZD",
]

# FX Pairs supported
FX_PAIRS = [
    {"pair": "EURUSD", "base": "EUR", "quote": "USD"},
    {"pair": "GBPUSD", "base": "GBP", "quote": "USD"},
    {"pair": "USDJPY", "base": "USD", "quote": "JPY"},
    {"pair": "AUDUSD", "base": "AUD", "quote": "USD"},
    {"pair": "NZDUSD", "base": "NZD", "quote": "USD"},
    {"pair": "USDCAD", "base": "USD", "quote": "CAD"},
    {"pair": "USDCHF", "base": "USD", "quote": "CHF"},
]

# NDIP Topics
NDIP_TOPICS = {
    "GLOBAL_FACTORS": "global.factors.snapshot",
    "MARKET_REGIME": "market.regime.snapshot",
    "MACRO_CONDITIONS": "macro.conditions.snapshot",
}

# Factor weights for currency strength
FACTOR_WEIGHTS = {
    "growth": 0.20,
    "inflation": 0.15,
    "rates": 0.20,
    "central_bank": 0.15,
    "risk_sentiment": 0.15,
    "liquidity": 0.10,
    "geopolitical": 0.05,
}
