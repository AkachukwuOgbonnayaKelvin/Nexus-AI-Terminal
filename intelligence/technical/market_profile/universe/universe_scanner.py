"""
Universe Scanner – fetches data for all symbols/timeframes from the Technical Data Platform.
"""

import logging
import pandas as pd

from ..data.profile_data import fetch_profile_data
from ..data.quality_gate import check_data_quality
from .asset_registry import AssetRegistry

logger = logging.getLogger(__name__)


class UniverseScanner:
    """
    Scans the entire asset universe and returns OHLC data for each symbol/timeframe
    that passes the data quality gate.
    """

    def __init__(
        self, data_platform, registry: AssetRegistry, quality_config, lookback_bars: int
    ):
        self.data_platform = data_platform
        self.registry = registry
        self.quality_config = quality_config
        self.lookback_bars = lookback_bars

    def scan(self, timeframe: str) -> dict[str, pd.DataFrame]:
        """
        Scan all symbols for the given timeframe.

        Returns:
            A dictionary mapping symbol -> OHLC DataFrame for symbols that
            passed the data quality gate. Symbols that fail are excluded.

        Raises:
            Exception: if a data access error occurs (propagated to engine).
        """
        symbols = self.registry.get_all_symbols()
        result = {}
        errors = []

        for symbol in symbols:
            try:
                # Fetch data using the lookback bars from config
                df = fetch_profile_data(
                    self.data_platform, symbol, timeframe, self.lookback_bars
                )
                if df is None or len(df) == 0:
                    logger.debug(f"No data for {symbol} {timeframe}")
                    continue

                # DEBUG: Log the max_stale_hours being used
                max_hours = self.quality_config.max_stale_hours.get(timeframe, "default")
                logger.info(f"DEBUG: {symbol} {timeframe} max_stale_hours={max_hours}")

                # Validate data quality
                quality = check_data_quality(
                    df,
                    symbol,
                    timeframe,
                    max_stale_hours=self.quality_config.max_stale_hours.get(
                        timeframe, 24.0
                    ),
                    min_bars=self.quality_config.min_bars,
                    max_gap_percentage=self.quality_config.max_gap_percentage,
                )
                if (
                    quality.status in ("fail", "partial")
                    and quality.status != "partial"
                ):
                    logger.debug(
                        f"Data quality failed for {symbol} {timeframe}: {quality.reason}"
                    )
                    continue

                result[symbol] = df

            except Exception as e:
                # Catch specific data access errors (e.g., connection failure)
                error_msg = f"Data access error for {symbol} {timeframe}: {e}"
                errors.append(error_msg)
                logger.error(error_msg)
                # Re-raise to propagate to engine; the engine will handle it
                raise

        if errors and not result:
            # If we have errors and no results, we should raise an exception
            # The engine will catch it and set system_status = "failed"
            if any(
                "connection" in e.lower() or "authentication" in e.lower()
                for e in errors
            ):
                raise Exception(f"Data access failure: {errors[0]}")

        return result
