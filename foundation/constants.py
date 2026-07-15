"""Platform constants and enums.

This module defines all constant values, enumerations, and immutable
configuration used across the platform.
"""

from enum import Enum


class Environment(str, Enum):
    """Application environment."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AssetClass(str, Enum):
    """Asset classes supported by the platform."""

    FOREX = "forex"
    EQUITY = "equity"
    COMMODITY = "commodity"
    BOND = "bond"
    CRYPTO = "crypto"
    INDEX = "index"
    OPTION = "option"
    FUTURE = "future"


class Timeframe(str, Enum):
    """Timeframes for market data."""

    TICK = "tick"
    SECOND = "1s"
    MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    HOUR = "1h"
    FOUR_HOURS = "4h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1M"


class MarketRegime(str, Enum):
    """Market regime classifications."""

    TRENDING_UP = "trending_up"
    TRENDING_DOWN = "trending_down"
    RANGING = "ranging"
    RISK_ON = "risk_on"
    RISK_OFF = "risk_off"
    VOLATILE = "volatile"
    QUIET = "quiet"


# Time constants
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400
SECONDS_PER_WEEK = 604800

# Default limits
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 1000

# Market sessions (UTC)
MARKET_SESSIONS = {
    "asia": {"open": 0, "close": 9},  # 0-9 UTC
    "london": {"open": 8, "close": 16},  # 8-16 UTC
    "new_york": {"open": 13, "close": 21},  # 13-21 UTC
}

# Supported currencies
MAJOR_CURRENCIES = ["USD", "EUR", "JPY", "GBP", "CHF", "CAD", "AUD", "NZD"]
MINOR_CURRENCIES = ["HKD", "SGD", "SEK", "NOK", "DKK", "MXN", "KRW", "ZAR"]

# Supported commodities
COMMODITIES = ["XAU", "XAG", "WTI", "BRENT", "NG", "COPPER"]

# Supported indices
INDICES = ["US30", "US500", "US100", "GER40", "UK100", "FRA40", "JP225", "HK50", "AU200"]
