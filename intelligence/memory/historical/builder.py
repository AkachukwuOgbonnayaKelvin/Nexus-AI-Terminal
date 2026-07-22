"""
Historical Memory Builder - Constructs Canonical Global Windows
"""

import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from .schemas import (
    HistoricalWindow,
    MarketState,
    AssetOutcome,
    AssetPrice,
    ForwardReturn,
)

logger = logging.getLogger(__name__)


class HistoricalMemoryBuilder:
    """
    Builds canonical global historical windows from per-symbol data.

    Input: Per-symbol historical windows (current format)
    Output: Global time-indexed windows (canonical format)
    """

    def __init__(self, min_coverage_ratio: float = 0.70):
        self.min_coverage_ratio = min_coverage_ratio
        self.raw_windows = []
        self.canonical_windows = []
        self._symbols = []
        self._timestamps = []

    def load_raw_windows(self, raw_windows: List[Dict]) -> None:
        """Load raw per-symbol windows"""
        self.raw_windows = raw_windows
        self._extract_symbols_and_timestamps()
        logger.info(f"Loaded {len(raw_windows)} raw windows")

    def _extract_symbols_and_timestamps(self) -> None:
        """Extract unique symbols and timestamps from raw data"""
        symbols = set()
        timestamps = set()

        for w in self.raw_windows:
            symbol = w.get("symbol", "UNKNOWN")
            symbols.add(symbol)

            # Try to get timestamp from window_dates
            window_dates = w.get("window_dates", [])
            if window_dates:
                # Use the first date as the window identifier
                timestamps.add(window_dates[0])

        self._symbols = list(symbols)
        self._timestamps = sorted(timestamps)

        logger.info(
            f"Found {len(self._symbols)} symbols and {len(self._timestamps)} timestamps"
        )

    def build_canonical_windows(self) -> List[HistoricalWindow]:
        """Build canonical global windows from raw data"""
        if not self.raw_windows:
            logger.warning("No raw windows loaded")
            return []

        # Group raw windows by timestamp
        windows_by_timestamp = defaultdict(list)

        for w in self.raw_windows:
            window_dates = w.get("window_dates", [])
            if window_dates:
                timestamp = window_dates[0]  # Use first date as key
                windows_by_timestamp[timestamp].append(w)

        logger.info(f"Grouped into {len(windows_by_timestamp)} timestamps")

        # Build canonical windows for each timestamp
        canonical_windows = []

        for timestamp, raw_windows in windows_by_timestamp.items():
            window = self._build_single_window(timestamp, raw_windows)
            if window and window.is_valid:
                canonical_windows.append(window)

        self.canonical_windows = canonical_windows
        logger.info(f"Built {len(canonical_windows)} valid canonical windows")

        return canonical_windows

    def _build_single_window(
        self, timestamp: Any, raw_windows: List[Dict]
    ) -> Optional[HistoricalWindow]:
        """Build a single canonical window from raw windows at a timestamp"""
        try:
            # Convert timestamp to string if needed
            timestamp_str = str(timestamp)
            window_id = f"WINDOW_{timestamp_str.replace('-', '_')}"

            # Parse timestamp
            if isinstance(timestamp, str):
                try:
                    dt = datetime.fromisoformat(timestamp)
                except Exception:
                    dt = datetime.utcnow()
            else:
                dt = datetime.utcnow()

            # Build market state from aggregated data
            market_state = self._build_market_state(raw_windows)

            # Build asset outcomes
            assets = {}
            for w in raw_windows:
                symbol = w.get("symbol", "UNKNOWN")
                price_data = self._extract_price_data(w)
                forward_returns = self._extract_forward_returns(w)

                if price_data:
                    assets[symbol] = AssetOutcome(
                        symbol=symbol, price=price_data, forward_returns=forward_returns
                    )

            # Calculate coverage
            total_assets = len(self._symbols)
            available_assets = len(assets)
            coverage_ratio = available_assets / total_assets if total_assets > 0 else 0

            # Validate
            is_valid = coverage_ratio >= self.min_coverage_ratio

            return HistoricalWindow(
                window_id=window_id,
                timestamp=dt,
                market_state=market_state,
                assets=assets,
                total_assets=total_assets,
                available_assets=available_assets,
                coverage_ratio=coverage_ratio,
                is_valid=is_valid,
                rejection_reason=None
                if is_valid
                else f"Coverage {coverage_ratio:.1%} below minimum {self.min_coverage_ratio:.1%}",
                metadata={
                    "raw_windows_count": len(raw_windows),
                    "symbols": list(assets.keys()),
                },
            )

        except Exception as e:
            logger.warning(f"Failed to build window for {timestamp}: {e}")
            return None

    def _build_market_state(self, raw_windows: List[Dict]) -> MarketState:
        """Build market state from raw windows"""
        # Aggregate across windows
        regimes = []
        macro_scores = []
        # volatility_scores = ...  # Unused

        for w in raw_windows:
            # Try to get regime from symbol inference or raw data
            symbol = w.get("symbol", "")
            if symbol in ["XAUUSD", "USDJPY", "USDCHF"]:
                regimes.append("RISK_OFF")
            elif symbol in ["US500", "US100", "AUDUSD", "NZDUSD"]:
                regimes.append("RISK_ON")
            else:
                regimes.append("NEUTRAL")

            # Use price action to estimate scores
            prices = w.get("window_prices", [])
            if prices:
                start_price = prices[0]
                end_price = prices[-1]
                change_pct = (
                    ((end_price - start_price) / start_price * 100)
                    if start_price > 0
                    else 0
                )

                if change_pct > 2:
                    macro_scores.append(60.0)
                elif change_pct > 0:
                    macro_scores.append(55.0)
                elif change_pct > -2:
                    macro_scores.append(45.0)
                else:
                    macro_scores.append(40.0)

        # Determine majority regime
        if regimes:
            from collections import Counter

            regime_counter = Counter(regimes)
            majority_regime = regime_counter.most_common(1)[0][0]
        else:
            majority_regime = "NEUTRAL"

        # Average scores
        avg_macro = sum(macro_scores) / len(macro_scores) if macro_scores else 50.0
        avg_volatility = 50.0  # Default

        return MarketState(
            regime=majority_regime,
            macro_score=avg_macro,
            central_bank_score=50.0,
            geopolitical_risk=50.0,
            capital_flow_score=50.0,
            sentiment_score=50.0,
            positioning_score=50.0,
            volatility_score=avg_volatility,
        )

    def _extract_price_data(self, w: Dict) -> Optional[AssetPrice]:
        """Extract price data from raw window"""
        prices = w.get("window_prices", [])
        if prices:
            # Use the last price in the window as the close
            close_price = prices[-1] if prices else 0
            return AssetPrice(
                close=close_price,
                open=prices[0] if prices else None,
                high=max(prices) if prices else None,
                low=min(prices) if prices else None,
            )
        return None

    def _extract_forward_returns(self, w: Dict) -> Dict[str, ForwardReturn]:
        """Extract forward returns from raw window"""
        forward_returns = {}
        raw_forward = w.get("forward_returns", {})

        for key, value in raw_forward.items():
            if value > 0.1:
                direction = "BULLISH"
            elif value < -0.1:
                direction = "BEARISH"
            else:
                direction = "NEUTRAL"

            forward_returns[key] = ForwardReturn(
                return_pct=value, direction=direction, win=value > 0, confidence=70.0
            )

        return forward_returns

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the built windows"""
        if not self.canonical_windows:
            return {"status": "NO_WINDOWS"}

        valid_windows = [w for w in self.canonical_windows if w.is_valid]
        invalid_windows = [w for w in self.canonical_windows if not w.is_valid]

        # Calculate asset coverage
        asset_coverage = {}
        for w in valid_windows:
            for symbol in w.assets.keys():
                asset_coverage[symbol] = asset_coverage.get(symbol, 0) + 1

        total_valid = len(valid_windows)
        for symbol in asset_coverage:
            asset_coverage[symbol] = (
                asset_coverage[symbol] / total_valid if total_valid > 0 else 0
            )

        return {
            "status": "READY",
            "total_raw_windows": len(self.raw_windows),
            "total_canonical_windows": len(self.canonical_windows),
            "valid_windows": len(valid_windows),
            "invalid_windows": len(invalid_windows),
            "symbols_count": len(self._symbols),
            "asset_coverage": asset_coverage,
            "coverage_ratio": total_valid / len(self.canonical_windows)
            if self.canonical_windows
            else 0,
        }

    def save_canonical_windows(self, filepath: str) -> None:
        """Save canonical windows to JSON file"""
        data = []
        for w in self.canonical_windows:
            data.append(w.dict())

        with open(filepath, "w") as f:
            json.dump(data, f, default=str)

        logger.info(f"Saved {len(data)} canonical windows to {filepath}")

    def get_canonical_windows(self) -> List[HistoricalWindow]:
        """Get the built canonical windows"""
        return self.canonical_windows
