"""Timeframe Resampler - Converts OHLCV to higher timeframes"""

from datetime import datetime

from providers.base import OHLCVData


class TimeframeResampler:
    """
    Resamples OHLCV data to higher timeframes.

    Input: M1 data
    Output: M5, M15, M30, H1, H4, D1, W1, MN1
    """

    TIMEFRAME_MAP = {
        "M1": 1,
        "M5": 5,
        "M15": 15,
        "M30": 30,
        "H1": 60,
        "H4": 240,
        "D1": 1440,
        "W1": 10080,
        "MN1": 43200,
    }

    def __init__(self):
        self._cache = {}

    def resample(self, bars: list[OHLCVData], target_timeframe: str) -> list[OHLCVData]:
        """
        Resample OHLCV data to a higher timeframe.

        Args:
            bars: List of OHLCVData (must be sorted by timestamp)
            target_timeframe: Target timeframe (e.g., 'H1', 'D1')

        Returns:
            List of resampled OHLCVData
        """
        if not bars:
            return []

        # Sort bars by timestamp
        sorted_bars = sorted(bars, key=lambda x: x.timestamp)

        # Get timeframe in minutes
        target_minutes = self.TIMEFRAME_MAP.get(target_timeframe, 60)
        source_minutes = self.TIMEFRAME_MAP.get(bars[0].timeframe, 1)

        # Calculate group size
        group_size = target_minutes // source_minutes
        if group_size < 1:
            return sorted_bars

        result = []
        current_group = []
        current_group_start = None

        for bar in sorted_bars:
            # Calculate the start of the group for this bar
            if current_group_start is None:
                current_group_start = self._get_group_start(
                    bar.timestamp, target_minutes
                )

            # Check if this bar belongs to the current group
            bar_group_start = self._get_group_start(bar.timestamp, target_minutes)

            if bar_group_start == current_group_start:
                current_group.append(bar)
            else:
                # Close the current group
                if current_group:
                    resampled = self._resample_group(
                        current_group, current_group_start, target_timeframe
                    )
                    if resampled:
                        result.append(resampled)

                # Start new group
                current_group = [bar]
                current_group_start = bar_group_start

        # Handle the last group
        if current_group:
            resampled = self._resample_group(
                current_group, current_group_start, target_timeframe
            )
            if resampled:
                result.append(resampled)

        return result

    def _get_group_start(self, timestamp: datetime, minutes: int) -> datetime:
        """Get the start of the group for a timestamp"""
        # Calculate the group start
        total_minutes = (timestamp.hour * 60) + timestamp.minute
        group_start_minute = (total_minutes // minutes) * minutes
        group_hour = group_start_minute // 60
        group_minute = group_start_minute % 60

        return timestamp.replace(
            hour=group_hour, minute=group_minute, second=0, microsecond=0
        )

    def _resample_group(
        self, group: list[OHLCVData], timestamp: datetime, timeframe: str
    ) -> OHLCVData | None:
        """Resample a group of bars into a single bar"""
        if not group:
            return None

        open_price = group[0].open
        high_price = max([b.high for b in group])
        low_price = min([b.low for b in group])
        close_price = group[-1].close
        total_volume = (
            sum([b.volume for b in group if b.volume is not None])
            if group[0].volume is not None
            else None
        )

        return OHLCVData(
            symbol=group[0].symbol,
            timeframe=timeframe,
            timestamp=timestamp,
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            volume=total_volume,
            source=group[0].source,
            quality_score=min([b.quality_score for b in group]) if group else 95.0,
        )

    def resample_all_timeframes(
        self, bars: list[OHLCVData]
    ) -> dict[str, list[OHLCVData]]:
        """Resample bars to all higher timeframes"""
        result = {}

        # Define target timeframes
        target_timeframes = ["M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"]

        for target in target_timeframes:
            if target != bars[0].timeframe:
                resampled = self.resample(bars, target)
                if resampled:
                    result[target] = resampled

        return result
