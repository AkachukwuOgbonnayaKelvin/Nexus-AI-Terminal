"""Universal Data Transport Object."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class UniversalTransport:
    """Universal Transport Object – standardized data from any provider."""

    # Core fields (required)
    asset: str
    value: float
    timestamp: datetime

    # Price fields (optional)
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None

    # Metadata
    source: str = "unknown"
    provider: str = "unknown"
    symbol_provider: Optional[str] = None  # Original symbol from provider

    # Classification (to be filled by adapter)
    asset_class: str = "unknown"

    # Raw data for audit
    raw_data: Dict[str, Any] = field(default_factory=dict)

    # Extra fields
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
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
