"""
GLB-005 Central Bank Intelligence Engine - Constants
"""

from enum import Enum


class PolicyStance(str, Enum):
    """Monetary policy stance"""

    HAWKISH = "HAWKISH"
    DOVISH = "DOVISH"
    NEUTRAL = "NEUTRAL"
    TRANSITIONING = "TRANSITIONING"


class PolicyRegime(str, Enum):
    """Overall policy regime"""

    TIGHTENING = "TIGHTENING"
    EASING = "EASING"
    HOLDING = "HOLDING"
    DIVERGENT = "DIVERGENT"


class BalanceSheetPolicy(str, Enum):
    """Balance sheet policy"""

    QT = "QT"  # Quantitative Tightening
    QE = "QE"  # Quantitative Easing
    HOLDING = "HOLDING"


class CentralBank(str, Enum):
    """Supported central banks"""

    FED = "FED"
    ECB = "ECB"
    BOJ = "BOJ"
    BOE = "BOE"
    SNB = "SNB"
    BOC = "BOC"
    RBA = "RBA"
    RBNZ = "RBNZ"
    PBOC = "PBOC"


# Central bank metadata
CENTRAL_BANK_METADATA = {
    "FED": {
        "name": "Federal Reserve",
        "currency": "USD",
        "region": "US",
        "rate": 5.50,
        "base_importance": 95,
        "policy_bias": "HAWKISH",
    },
    "ECB": {
        "name": "European Central Bank",
        "currency": "EUR",
        "region": "EU",
        "rate": 4.50,
        "base_importance": 88,
        "policy_bias": "NEUTRAL",
    },
    "BOJ": {
        "name": "Bank of Japan",
        "currency": "JPY",
        "region": "JP",
        "rate": 0.10,
        "base_importance": 75,
        "policy_bias": "DOVISH",
    },
    "BOE": {
        "name": "Bank of England",
        "currency": "GBP",
        "region": "UK",
        "rate": 5.25,
        "base_importance": 85,
        "policy_bias": "NEUTRAL",
    },
    "SNB": {
        "name": "Swiss National Bank",
        "currency": "CHF",
        "region": "CH",
        "rate": 1.75,
        "base_importance": 65,
        "policy_bias": "NEUTRAL",
    },
    "BOC": {
        "name": "Bank of Canada",
        "currency": "CAD",
        "region": "CA",
        "rate": 5.00,
        "base_importance": 70,
        "policy_bias": "NEUTRAL",
    },
    "RBA": {
        "name": "Reserve Bank of Australia",
        "currency": "AUD",
        "region": "AU",
        "rate": 4.35,
        "base_importance": 70,
        "policy_bias": "NEUTRAL",
    },
    "RBNZ": {
        "name": "Reserve Bank of New Zealand",
        "currency": "NZD",
        "region": "NZ",
        "rate": 5.50,
        "base_importance": 65,
        "policy_bias": "NEUTRAL",
    },
    "PBOC": {
        "name": "People's Bank of China",
        "currency": "CNY",
        "region": "CN",
        "rate": 3.45,
        "base_importance": 60,
        "policy_bias": "DOVISH",
    },
}

# NDIP Topics
NDIP_TOPICS = {
    "CENTRAL_BANK_DATA": "central.bank.policy",
    "RATE_DATA": "central.bank.rates",
    "MARKET_DATA": "market.price.snapshot",
}

# Asset classes affected by central bank policy
ASSET_CLASS_EXPOSURE = {
    "FX": 1.0,
    "BONDS": 0.85,
    "EQUITIES": 0.60,
    "COMMODITIES": 0.40,
    "CRYPTO": 0.20,
}
