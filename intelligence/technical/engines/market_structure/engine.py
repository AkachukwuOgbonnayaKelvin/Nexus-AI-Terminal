from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from intelligence.technical.contracts import EngineBias, MarketRegime, TechnicalSignal
from intelligence.technical.data_access import TechnicalDataPlatform


@dataclass
class SwingPoint:
    time: datetime
    price: float
    type: str
    strength: float
    left_bars: int
    right_bars: int


class MarketStructureEngine:
    def __init__(self, data_platform: TechnicalDataPlatform):
        self.data = data_platform
        self.config = {
            "swing_lookback": 5,
            "min_swing_distance": 3,
            "min_bars_required": 50,
        }

    def analyze(
        self, symbol: str, timeframe: str = "H1", lookback_bars: int = 200
    ) -> TechnicalSignal:
        df = self.data.get_last_bars(symbol, timeframe, lookback_bars)

        if df.empty:
            return self._empty_signal(
                symbol, timeframe, "No data found in technical store"
            )

        if len(df) < self.config["min_bars_required"]:
            return self._empty_signal(
                symbol,
                timeframe,
                f"Insufficient data: {len(df)} bars found, minimum {self.config['min_bars_required']} required",
            )

        df = df.tail(lookback_bars)

        swings = self._detect_swings(df)
        structure = self._classify_structure(df, swings)
        events = self._detect_events(df, swings)
        bias, confidence = self._determine_bias(structure, events)
        levels = self._get_key_levels(swings)

        return TechnicalSignal(
            engine="market_structure",
            symbol=symbol,
            timeframe=timeframe,
            timestamp=datetime.now(),
            bias=bias,
            direction="long"
            if bias == EngineBias.BULLISH
            else "short"
            if bias == EngineBias.BEARISH
            else "neutral",
            confidence=confidence,
            regime=structure.get("regime", MarketRegime.UNKNOWN),
            regime_confidence=structure.get("regime_confidence", 0.5),
            key_levels=levels,
            events=events,
            invalidation_level=self._get_invalidation_level(swings, bias),
            invalidation_condition=self._get_invalidation_condition(bias),
            reasoning=self._build_reasoning(structure, events),
            data_quality=self._check_data_quality(df),
            data_range_start=df["time"].iloc[0] if not df.empty else None,
            data_range_end=df["time"].iloc[-1] if not df.empty else None,
            extras={
                "swings": swings[-20:],
                "bars_analyzed": len(df),
                "bars_requested": lookback_bars,
                "data_status": "OK",
            },
        )

    def _detect_swings(self, df: pd.DataFrame) -> list[SwingPoint]:
        if len(df) < self.config["swing_lookback"] * 2:
            return []
        highs = df["high"].values
        lows = df["low"].values
        times = df["time"].values  # numpy datetime64
        lookback = self.config["swing_lookback"]
        swings = []

        for i in range(lookback, len(df) - lookback):
            if highs[i] == max(highs[i - lookback : i + lookback + 1]):
                left_high = max(highs[i - lookback : i])
                right_high = max(highs[i + 1 : i + lookback + 1])
                if highs[i] > left_high and highs[i] > right_high:
                    strength = self._calc_strength(df, i, "high")
                    # Convert numpy datetime64 to Python datetime
                    swing_time = pd.to_datetime(times[i]).to_pydatetime()
                    swings.append(
                        SwingPoint(
                            swing_time, highs[i], "high", strength, lookback, lookback
                        )
                    )
            if lows[i] == min(lows[i - lookback : i + lookback + 1]):
                left_low = min(lows[i - lookback : i])
                right_low = min(lows[i + 1 : i + lookback + 1])
                if lows[i] < left_low and lows[i] < right_low:
                    strength = self._calc_strength(df, i, "low")
                    swing_time = pd.to_datetime(times[i]).to_pydatetime()
                    swings.append(
                        SwingPoint(
                            swing_time, lows[i], "low", strength, lookback, lookback
                        )
                    )

        if len(swings) > 1:
            filtered = [swings[0]]
            for swing in swings[1:]:
                last = filtered[-1]
                delta_seconds = (swing.time - last.time).total_seconds()
                if abs(delta_seconds) / 60 >= self.config["min_swing_distance"]:
                    filtered.append(swing)
            swings = filtered
        return swings

    def _calc_strength(self, df, idx, swing_type):
        lookback = self.config["swing_lookback"]
        start_idx = max(0, idx - lookback)
        end_idx = min(len(df), idx + lookback + 1)
        if swing_type == "high":
            surrounding = df["high"].iloc[start_idx:end_idx].max()
            base = df["high"].iloc[idx]
            if surrounding > base:
                return min(1.0, (surrounding - base) / base * 10)
            return 0.3
        else:
            surrounding = df["low"].iloc[start_idx:end_idx].min()
            base = df["low"].iloc[idx]
            if surrounding < base:
                return min(1.0, (base - surrounding) / base * 10)
            return 0.3

    def _classify_structure(self, df, swings):
        if len(swings) < 4:
            return {
                "regime": MarketRegime.UNKNOWN,
                "regime_confidence": 0.0,
                "trend_strength": 0.0,
            }
        bullish = 0
        bearish = 0
        for i in range(2, len(swings)):
            s = swings[i]
            p = swings[i - 1]
            p2 = swings[i - 2]
            if s.type == "high" and p.type == "high":
                if s.price > p.price > p2.price:
                    bullish += 1
                elif s.price < p.price < p2.price:
                    bearish += 1
        total = bullish + bearish
        if total == 0:
            regime = MarketRegime.RANGING
            conf = 0.6
        elif bullish > bearish:
            regime = MarketRegime.TRENDING_UP
            conf = 0.5 + 0.4 * (bullish / total)
        elif bearish > bullish:
            regime = MarketRegime.TRENDING_DOWN
            conf = 0.5 + 0.4 * (bearish / total)
        else:
            regime = MarketRegime.RANGING
            conf = 0.6
        return {
            "regime": regime,
            "regime_confidence": min(1.0, conf),
            "trend_strength": abs(bullish - bearish) / max(1, total),
        }

    def _detect_events(self, df, swings):
        events = []
        if len(swings) < 4:
            return events

        for i in range(3, len(swings)):
            if swings[i].type == "high" and swings[i].price > swings[i - 2].price:
                events.append(
                    {
                        "type": "bos_bullish",
                        "level": swings[i].price,
                        "time": swings[i].time,
                        "significance": 0.8,
                        "broken_level": swings[i - 2].price,
                        "event_type": "BOS_BULLISH",
                    }
                )
            if swings[i].type == "low" and swings[i].price < swings[i - 2].price:
                events.append(
                    {
                        "type": "bos_bearish",
                        "level": swings[i].price,
                        "time": swings[i].time,
                        "significance": 0.8,
                        "broken_level": swings[i - 2].price,
                        "event_type": "BOS_BEARISH",
                    }
                )

        # CHoCH detection
        if len(swings) >= 6:
            last_two_highs = [s for s in swings if s.type == "high"][-2:]
            last_two_lows = [s for s in swings if s.type == "low"][-2:]
            if len(last_two_highs) >= 2 and len(last_two_lows) >= 2:
                if (
                    last_two_highs[-1].price < last_two_highs[-2].price
                    and last_two_lows[-1].price < last_two_lows[-2].price
                ):
                    events.append(
                        {
                            "type": "choch",
                            "level": last_two_highs[-1].price,
                            "time": last_two_highs[-1].time,
                            "significance": 0.85,
                            "broken_level": last_two_highs[-2].price,
                            "event_type": "CHOCH",
                        }
                    )

        return events

    def _determine_bias(self, structure, events):
        regime = structure.get("regime", MarketRegime.UNKNOWN)
        conf = structure.get("regime_confidence", 0.5)

        if regime == MarketRegime.TRENDING_UP:
            return EngineBias.BULLISH, conf
        elif regime == MarketRegime.TRENDING_DOWN:
            return EngineBias.BEARISH, conf
        else:
            recent = [
                e
                for e in events
                if e["type"] in ["bos_bullish", "bos_bearish", "choch"]
            ]
            if recent:
                last_event = recent[-1]
                if "bullish" in last_event["type"] or last_event["type"] == "choch":
                    return EngineBias.BULLISH, 0.65
                else:
                    return EngineBias.BEARISH, 0.65
            return EngineBias.NEUTRAL, 0.5

    def _get_key_levels(self, swings):
        levels = []
        recent = swings[-7:] if len(swings) > 7 else swings
        for s in recent:
            strength = s.strength
            recency_boost = (
                0.1 * (len(recent) - list(recent).index(s)) / len(recent)
                if recent
                else 0
            )
            total_strength = min(1.0, strength + recency_boost)
            levels.append(
                {
                    "level": s.price,
                    "type": "resistance" if s.type == "high" else "support",
                    "strength": round(total_strength, 3),
                    "timestamp": s.time.isoformat()
                    if hasattr(s.time, "isoformat")
                    else str(s.time),
                    "components": {
                        "base_strength": strength,
                        "recency_boost": recency_boost,
                        "touch_count": 1,
                    },
                }
            )
        return levels

    def _get_invalidation_level(self, swings, bias):
        if not swings:
            return None
        if bias == EngineBias.BULLISH:
            lows = [s for s in swings if s.type == "low"]
            return lows[-1].price if lows else None
        elif bias == EngineBias.BEARISH:
            highs = [s for s in swings if s.type == "high"]
            return highs[-1].price if highs else None
        return None

    def _get_invalidation_condition(self, bias):
        if bias == EngineBias.BULLISH:
            return "Break below the last protected higher low"
        elif bias == EngineBias.BEARISH:
            return "Break above the last protected lower high"
        return None

    def _build_reasoning(self, structure, events):
        reasons = []
        regime = structure.get("regime", MarketRegime.UNKNOWN)
        reasons.append(f"Market regime: {regime.value}")

        for e in events[-3:]:
            level_desc = f"{e['level']:.5f}"
            if e["type"] == "choch":
                reasons.append(f"Detected: Change of Character at {level_desc}")
            else:
                reasons.append(f"Detected: {e['type']} at {level_desc}")

        if structure.get("trend_strength", 0) > 0.3:
            reasons.append(f"Trend strength: {structure['trend_strength']:.2f}")

        return reasons

    def _check_data_quality(self, df):
        if df.empty:
            return 0.0
        time_diff = df["time"].diff().dropna()
        expected = time_diff.mode()
        if not expected.empty:
            gaps = time_diff > expected.iloc[0] * 2
            gap_ratio = gaps.sum() / len(df)
            quality = 1.0 - min(1.0, gap_ratio * 5)
        else:
            quality = 1.0
        invalid = (df["high"] < df["low"]).sum() if "high" in df and "low" in df else 0
        quality *= 1.0 - invalid / max(1, len(df))
        return max(0.0, min(1.0, quality))

    def _empty_signal(self, symbol, timeframe, reason="Insufficient data for analysis"):
        return TechnicalSignal(
            engine="market_structure",
            symbol=symbol,
            timeframe=timeframe,
            timestamp=datetime.now(),
            bias=EngineBias.UNKNOWN,
            direction="neutral",
            confidence=0.0,
            regime=MarketRegime.UNKNOWN,
            regime_confidence=0.0,
            key_levels=[],
            events=[],
            invalidation_level=None,
            invalidation_condition=None,
            reasoning=[reason],
            data_quality=0.0,
            extras={"data_status": "UNAVAILABLE", "reason": reason},
        )
