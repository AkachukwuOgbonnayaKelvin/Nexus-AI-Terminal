"""Universal Data Transport Object."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class UniversalTransport:
    """Universal Transport Object – standardized data from any provider."""

    # Core fields (required)
    asset: str
    value: float
    timestamp: datetime

    # Price fields (optional)
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    volume: int | None = None

    # Metadata
    source: str = "unknown"
    provider: str = "unknown"
    symbol_provider: str | None = None  # Original symbol from provider

    # Classification (to be filled by adapter)
    asset_class: str = "unknown"

    # Raw data for audit
    raw_data: dict[str, Any] = field(default_factory=dict)

    # Extra fields
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for NDIP ingestion."""
        return {
            "asset": self.asset,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "source": self.source,
            "asset_class": self.asset_class,
            "metadata": self.metadata,
        }
