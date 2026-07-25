"""
Canonical contracts for technical data.
Ensures every engine receives a typed, predictable structure.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OHLCVBar:
    """Canonical OHLCV bar."""

    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None

    def __post_init__(self):
        # Validate OHLC
        if self.high < self.low:
            raise ValueError(f"High < Low: {self.high} < {self.low}")
        if self.high < self.open or self.high < self.close:
            raise ValueError(f"High invalid: {self.high}")
        if self.low > self.open or self.low > self.close:
            raise ValueError(f"Low invalid: {self.low}")
        if self.open <= 0 or self.high <= 0 or self.low <= 0 or self.close <= 0:
            raise ValueError("Prices must be positive")


@dataclass(frozen=True)
class OHLCVSeries:
    """A series of OHLCV bars for a symbol and timeframe."""

    symbol: str
    timeframe: str
    bars: list[OHLCVBar]
    coverage_start: datetime | None = None
    coverage_end: datetime | None = None

    def __len__(self):
        return len(self.bars)

    def __getitem__(self, idx):
        return self.bars[idx]


@dataclass(frozen=True)
class TickBar:
    """Canonical tick data."""

    symbol: str
    timestamp: datetime
    price: float
    volume: float | None = None
    bid: float | None = None
    ask: float | None = None


@dataclass(frozen=True)
class VolumeBar:
    """Canonical volume data."""

    symbol: str
    timeframe: str
    timestamp: datetime
    volume: float
    baseline: float | None = None
    z_score: float | None = None
    regime: str | None = None
