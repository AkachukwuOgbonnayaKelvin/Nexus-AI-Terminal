"""Platform settings management.

This module provides runtime settings that can be modified during execution.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Settings:
    """Runtime settings."""

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json or text
    log_to_file: bool = True
    log_to_console: bool = True

    # Data
    data_retention_days: int = 365
    cache_ttl_seconds: int = 300
    batch_size: int = 1000

    # Analysis
    default_timeframe: str = "1d"
    max_analysis_periods: int = 1000
    confidence_threshold: float = 0.6

    # Notifications
    enable_notifications: bool = True
    notification_level: str = "info"

    # Performance
    enable_profiling: bool = False
    max_workers: int = 4

    # Feature flags
    features: dict[str, bool] = field(
        default_factory=lambda: {
            "experimental_ai": False,
            "live_trading": False,
            "backtesting": True,
            "sentiment_analysis": True,
        }
    )

    def update(self, **kwargs: Any) -> None:
        """Update settings with keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "log_level": self.log_level,
            "log_format": self.log_format,
            "data_retention_days": self.data_retention_days,
            "cache_ttl_seconds": self.cache_ttl_seconds,
            "default_timeframe": self.default_timeframe,
            "confidence_threshold": self.confidence_threshold,
            "features": self.features,
        }


# Global settings instance
settings = Settings()
