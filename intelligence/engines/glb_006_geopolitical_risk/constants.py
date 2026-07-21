"""
GLB-006 Geopolitical Risk Intelligence Engine - Constants
"""

from enum import Enum


class GeopoliticalEventType(str, Enum):
    """Types of geopolitical events"""

    MILITARY_CONFLICT = "MILITARY_CONFLICT"
    SANCTIONS = "SANCTIONS"
    ELECTION = "ELECTION"
    DIPLOMATIC_CRISIS = "DIPLOMATIC_CRISIS"
    TRADE_RESTRICTION = "TRADE_RESTRICTION"
    POLITICAL_INSTABILITY = "POLITICAL_INSTABILITY"
    TERRORISM = "TERRORISM"
    CYBER_ATTACK = "CYBER_ATTACK"
    SUPPLY_CHAIN_DISRUPTION = "SUPPLY_CHAIN_DISRUPTION"


class RiskSeverity(str, Enum):
    """Risk severity levels"""

    LOW = "LOW"
    MODERATE = "MODERATE"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskTrend(str, Enum):
    """Risk trend direction"""

    RISING = "RISING"
    FALLING = "FALLING"
    STABLE = "STABLE"


class TransmissionChannel(str, Enum):
    """Risk transmission channels"""

    RISK_OFF = "RISK_OFF"
    SAFE_HAVEN = "SAFE_HAVEN"
    ENERGY_SUPPLY = "ENERGY_SUPPLY"
    TRADE_DISRUPTION = "TRADE_DISRUPTION"
    INFLATION_SHOCK = "INFLATION_SHOCK"
    DEMAND_SHOCK = "DEMAND_SHOCK"
    SUPPLY_SHOCK = "SUPPLY_SHOCK"


# Country strategic importance scores (0-100)
STRATEGIC_IMPORTANCE = {
    "US": 95,
    "CN": 90,
    "RU": 85,
    "SA": 80,
    "DE": 75,
    "GB": 70,
    "FR": 65,
    "JP": 70,
    "IN": 65,
    "BR": 55,
    "IR": 50,
    "IL": 45,
    "KR": 55,
    "TW": 50,
    "UA": 40,
}

# Region strategic importance scores (0-100)
REGION_IMPORTANCE = {
    "MIDDLE_EAST": 90,
    "EAST_ASIA": 85,
    "EUROPE": 80,
    "NORTH_AMERICA": 75,
    "SOUTH_ASIA": 65,
    "LATIN_AMERICA": 50,
    "AFRICA": 45,
}

# NDIP Topics
NDIP_TOPICS = {
    "GEOPOLITICAL_EVENTS": "geopolitical.events",
    "NEWS_DATA": "news.feed",
    "GOVERNMENT_DATA": "government.statements",
}

# Event type severity base scores
EVENT_SEVERITY_BASE = {
    GeopoliticalEventType.MILITARY_CONFLICT: 85,
    GeopoliticalEventType.SANCTIONS: 65,
    GeopoliticalEventType.ELECTION: 40,
    GeopoliticalEventType.DIPLOMATIC_CRISIS: 60,
    GeopoliticalEventType.TRADE_RESTRICTION: 55,
    GeopoliticalEventType.POLITICAL_INSTABILITY: 50,
    GeopoliticalEventType.TERRORISM: 70,
    GeopoliticalEventType.CYBER_ATTACK: 45,
    GeopoliticalEventType.SUPPLY_CHAIN_DISRUPTION: 60,
}

# Asset exposure to geopolitical risk - DIRECT MAPPING
ASSET_EXPOSURE = {
    # Safe havens (positive)
    "XAUUSD": {"risk_off": 0.95, "safe_haven": 0.95},
    "USDCHF": {"risk_off": 0.85, "safe_haven": 0.85},
    "USDJPY": {"risk_off": 0.80, "safe_haven": 0.80},
    # Risk currencies (negative)
    "AUDUSD": {"risk_off": -0.80, "trade": -0.60},
    "NZDUSD": {"risk_off": -0.75, "trade": -0.55},
    "USDCAD": {"risk_off": -0.60, "oil": 0.65},
    "EURUSD": {"risk_off": -0.50, "trade": -0.40},
    "GBPUSD": {"risk_off": -0.45, "trade": -0.35},
    # Commodities
    "WTI": {"oil": 0.90, "supply_shock": 0.85},
    "BRENT": {"oil": 0.90, "supply_shock": 0.85},
    "XAGUSD": {"risk_off": -0.40, "safe_haven": 0.50},
    "NGAS": {"supply_shock": 0.70},
    "COPPER": {"trade": -0.50},
    # Equities (negative)
    "US500": {"risk_off": -0.85, "trade": -0.50},
    "US100": {"risk_off": -0.90, "trade": -0.45},
    "US30": {"risk_off": -0.80, "trade": -0.45},
    "GER40": {"risk_off": -0.80, "trade": -0.55},
    "UK100": {"risk_off": -0.75, "oil": 0.40, "trade": -0.40},
    "JP225": {"risk_off": -0.70, "trade": -0.50},
}
