"""
GLB-009 - Historical Window Converter
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Any

from .input.schemas import (
    AssetPriceSeries,
    EnvironmentState,
    ForwardReturn,
    HistoricalWindow,
)

logger = logging.getLogger(__name__)


class WindowConverter:
    """Convert raw JSON windows to HistoricalWindow objects"""

    def __init__(self):
        self.converted = 0
        self.errors = 0

    def convert(self, raw_window: dict[str, Any]) -> HistoricalWindow | None:
        """
        Convert a raw window dictionary to a HistoricalWindow object.

        Args:
            raw_window: Raw window from JSON

        Returns:
            HistoricalWindow or None if conversion fails
        """
        try:
            # Extract symbol and prices
            symbol = raw_window.get("symbol", "UNKNOWN")
            close_prices = raw_window.get("window_prices", [])

            if not close_prices:
                return None

            # Create asset price series
            asset_prices = {symbol: AssetPriceSeries(close=close_prices)}

            # Convert forward returns
            forward_returns = {}
            for key, value in raw_window.get("forward_returns", {}).items():
                # Determine direction
                if value > 0.1:
                    direction = "BULLISH"
                elif value < -0.1:
                    direction = "BEARISH"
                else:
                    direction = "NEUTRAL"

                forward_returns[key] = ForwardReturn(
                    return_pct=value,
                    direction=direction,
                    win=value > 0,
                    confidence=70.0,
                )

            # Create environment state
            environment = EnvironmentState(regime=self._infer_regime(symbol))

            # Create window
            window = HistoricalWindow(
                window_id=f"WINDOW_{uuid.uuid4().hex[:8]}",
                timestamp=datetime.now() - timedelta(days=len(close_prices)),
                environment=environment,
                asset_prices=asset_prices,
                forward_returns=forward_returns,
                symbol=symbol,
                window_size=len(close_prices),
            )

            self.converted += 1
            return window

        except Exception as e:
            self.errors += 1
            logger.debug(f"Conversion error: {e}")
            return None

    def _infer_regime(self, symbol: str) -> str:
        """Infer regime from symbol"""
        safe_haven = ["XAUUSD", "USDJPY", "USDCHF", "CHFJPY"]
        risk_assets = ["US500", "US100", "US30", "AUDUSD", "NZDUSD", "AUDJPY"]

        if symbol in safe_haven:
            return "RISK_OFF"
        elif symbol in risk_assets:
            return "RISK_ON"
        return "NEUTRAL"

    def convert_batch(self, raw_windows: list[dict]) -> list[HistoricalWindow]:
        """Convert a batch of raw windows"""
        results = []
        for raw in raw_windows:
            window = self.convert(raw)
            if window:
                results.append(window)

        logger.info(f"Converted {len(results)} windows with {self.errors} errors")
        return results
