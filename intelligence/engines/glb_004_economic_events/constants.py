"""
GLB-004 Economic Events Intelligence Engine - Constants
"""

from enum import Enum


class EventImpact(str, Enum):
    """Event impact level"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class EventCategory(str, Enum):
    """Event category"""

    INFLATION = "INFLATION"
    EMPLOYMENT = "EMPLOYMENT"
    GROWTH = "GROWTH"
    CENTRAL_BANK = "CENTRAL_BANK"
    CONSUMER = "CONSUMER"
    MANUFACTURING = "MANUFACTURING"
    HOUSING = "HOUSING"
    TRADE = "TRADE"


class EventDirection(str, Enum):
    """Direction of event impact - INTERNAL USE ONLY"""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    CONDITIONAL = "CONDITIONAL"  # Impact depends on actual vs forecast


class EventStatus(str, Enum):
    """Event status"""

    UPCOMING = "UPCOMING"
    RELEASED = "RELEASED"
    REVISED = "REVISED"


# Canonical Asset Directions (for Hub output)
class AssetDirection(str, Enum):
    """Canonical asset directions - HUB OUTPUT ONLY"""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


# Event Taxonomy
EVENT_TAXONOMY = {
    EventCategory.INFLATION: {
        "CPI": {
            "base_importance": 85,
            "currency": "USD",
            "category": EventCategory.INFLATION,
        },
        "Core CPI": {
            "base_importance": 80,
            "currency": "USD",
            "category": EventCategory.INFLATION,
        },
        "PCE": {
            "base_importance": 82,
            "currency": "USD",
            "category": EventCategory.INFLATION,
        },
        "Core PCE": {
            "base_importance": 78,
            "currency": "USD",
            "category": EventCategory.INFLATION,
        },
        "PPI": {
            "base_importance": 70,
            "currency": "USD",
            "category": EventCategory.INFLATION,
        },
        "ECB CPI": {
            "base_importance": 75,
            "currency": "EUR",
            "category": EventCategory.INFLATION,
        },
        "UK CPI": {
            "base_importance": 75,
            "currency": "GBP",
            "category": EventCategory.INFLATION,
        },
        "Japan CPI": {
            "base_importance": 60,
            "currency": "JPY",
            "category": EventCategory.INFLATION,
        },
    },
    EventCategory.EMPLOYMENT: {
        "NFP": {
            "base_importance": 88,
            "currency": "USD",
            "category": EventCategory.EMPLOYMENT,
        },
        "Unemployment Rate": {
            "base_importance": 82,
            "currency": "USD",
            "category": EventCategory.EMPLOYMENT,
        },
        "Jobless Claims": {
            "base_importance": 65,
            "currency": "USD",
            "category": EventCategory.EMPLOYMENT,
        },
        "ADP Employment": {
            "base_importance": 60,
            "currency": "USD",
            "category": EventCategory.EMPLOYMENT,
        },
        "Average Hourly Earnings": {
            "base_importance": 72,
            "currency": "USD",
            "category": EventCategory.EMPLOYMENT,
        },
        "UK Employment": {
            "base_importance": 65,
            "currency": "GBP",
            "category": EventCategory.EMPLOYMENT,
        },
        "Eurozone Employment": {
            "base_importance": 60,
            "currency": "EUR",
            "category": EventCategory.EMPLOYMENT,
        },
    },
    EventCategory.GROWTH: {
        "GDP": {
            "base_importance": 85,
            "currency": "USD",
            "category": EventCategory.GROWTH,
        },
        "GDP Growth": {
            "base_importance": 80,
            "currency": "USD",
            "category": EventCategory.GROWTH,
        },
        "Retail Sales": {
            "base_importance": 72,
            "currency": "USD",
            "category": EventCategory.GROWTH,
        },
        "Industrial Production": {
            "base_importance": 65,
            "currency": "USD",
            "category": EventCategory.GROWTH,
        },
        "UK GDP": {
            "base_importance": 70,
            "currency": "GBP",
            "category": EventCategory.GROWTH,
        },
        "Eurozone GDP": {
            "base_importance": 70,
            "currency": "EUR",
            "category": EventCategory.GROWTH,
        },
        "Japan GDP": {
            "base_importance": 60,
            "currency": "JPY",
            "category": EventCategory.GROWTH,
        },
    },
    EventCategory.CENTRAL_BANK: {
        "Interest Rate Decision": {
            "base_importance": 95,
            "currency": "USD",
            "category": EventCategory.CENTRAL_BANK,
        },
        "FOMC Statement": {
            "base_importance": 92,
            "currency": "USD",
            "category": EventCategory.CENTRAL_BANK,
        },
        "ECB Rate Decision": {
            "base_importance": 88,
            "currency": "EUR",
            "category": EventCategory.CENTRAL_BANK,
        },
        "BOE Rate Decision": {
            "base_importance": 85,
            "currency": "GBP",
            "category": EventCategory.CENTRAL_BANK,
        },
        "BOJ Rate Decision": {
            "base_importance": 75,
            "currency": "JPY",
            "category": EventCategory.CENTRAL_BANK,
        },
        "RBA Rate Decision": {
            "base_importance": 70,
            "currency": "AUD",
            "category": EventCategory.CENTRAL_BANK,
        },
        "BOC Rate Decision": {
            "base_importance": 70,
            "currency": "CAD",
            "category": EventCategory.CENTRAL_BANK,
        },
        "SNB Rate Decision": {
            "base_importance": 65,
            "currency": "CHF",
            "category": EventCategory.CENTRAL_BANK,
        },
    },
    EventCategory.CONSUMER: {
        "Consumer Confidence": {
            "base_importance": 60,
            "currency": "USD",
            "category": EventCategory.CONSUMER,
        },
        "Consumer Sentiment": {
            "base_importance": 55,
            "currency": "USD",
            "category": EventCategory.CONSUMER,
        },
        "Personal Spending": {
            "base_importance": 58,
            "currency": "USD",
            "category": EventCategory.CONSUMER,
        },
    },
    EventCategory.MANUFACTURING: {
        "ISM Manufacturing": {
            "base_importance": 70,
            "currency": "USD",
            "category": EventCategory.MANUFACTURING,
        },
        "ISM Services": {
            "base_importance": 68,
            "currency": "USD",
            "category": EventCategory.MANUFACTURING,
        },
        "PMI Manufacturing": {
            "base_importance": 65,
            "currency": "USD",
            "category": EventCategory.MANUFACTURING,
        },
        "PMI Services": {
            "base_importance": 62,
            "currency": "USD",
            "category": EventCategory.MANUFACTURING,
        },
        "Eurozone PMI": {
            "base_importance": 60,
            "currency": "EUR",
            "category": EventCategory.MANUFACTURING,
        },
        "UK PMI": {
            "base_importance": 58,
            "currency": "GBP",
            "category": EventCategory.MANUFACTURING,
        },
    },
    EventCategory.HOUSING: {
        "Housing Starts": {
            "base_importance": 50,
            "currency": "USD",
            "category": EventCategory.HOUSING,
        },
        "Building Permits": {
            "base_importance": 45,
            "currency": "USD",
            "category": EventCategory.HOUSING,
        },
        "Existing Home Sales": {
            "base_importance": 45,
            "currency": "USD",
            "category": EventCategory.HOUSING,
        },
    },
    EventCategory.TRADE: {
        "Trade Balance": {
            "base_importance": 50,
            "currency": "USD",
            "category": EventCategory.TRADE,
        },
        "Current Account": {
            "base_importance": 45,
            "currency": "USD",
            "category": EventCategory.TRADE,
        },
    },
}


# Event Direction Map - How events affect assets (INTERNAL)
EVENT_DIRECTION_MAP = {
    "CPI": {
        "higher": {
            "USD": EventDirection.BULLISH,
            "YIELDS": EventDirection.BULLISH,
            "GOLD": EventDirection.BEARISH,
            "EQUITIES": EventDirection.BEARISH,
            "BONDS": EventDirection.BEARISH,
        },
        "lower": {
            "USD": EventDirection.BEARISH,
            "YIELDS": EventDirection.BEARISH,
            "GOLD": EventDirection.BULLISH,
            "EQUITIES": EventDirection.BULLISH,
            "BONDS": EventDirection.BULLISH,
        },
    },
    "NFP": {
        "higher": {
            "USD": EventDirection.BULLISH,
            "YIELDS": EventDirection.BULLISH,
            "GOLD": EventDirection.BEARISH,
            "EQUITIES": EventDirection.CONDITIONAL,
            "BONDS": EventDirection.BEARISH,
        },
        "lower": {
            "USD": EventDirection.BEARISH,
            "YIELDS": EventDirection.BEARISH,
            "GOLD": EventDirection.BULLISH,
            "EQUITIES": EventDirection.CONDITIONAL,
            "BONDS": EventDirection.BULLISH,
        },
    },
    "GDP": {
        "higher": {
            "USD": EventDirection.BULLISH,
            "YIELDS": EventDirection.BULLISH,
            "GOLD": EventDirection.BEARISH,
            "EQUITIES": EventDirection.BULLISH,
            "BONDS": EventDirection.BEARISH,
        },
        "lower": {
            "USD": EventDirection.BEARISH,
            "YIELDS": EventDirection.BEARISH,
            "GOLD": EventDirection.BULLISH,
            "EQUITIES": EventDirection.BEARISH,
            "BONDS": EventDirection.BULLISH,
        },
    },
    "Interest Rate Decision": {
        "higher": {
            "USD": EventDirection.BULLISH,
            "YIELDS": EventDirection.BULLISH,
            "GOLD": EventDirection.BEARISH,
            "EQUITIES": EventDirection.BEARISH,
            "BONDS": EventDirection.BEARISH,
        },
        "lower": {
            "USD": EventDirection.BEARISH,
            "YIELDS": EventDirection.BEARISH,
            "GOLD": EventDirection.BULLISH,
            "EQUITIES": EventDirection.BULLISH,
            "BONDS": EventDirection.BULLISH,
        },
    },
}

# NDIP Topics
NDIP_TOPICS = {
    "ECONOMIC_EVENTS": "economic.calendar.events",
    "MARKET_DATA": "market.price.snapshot",
}
