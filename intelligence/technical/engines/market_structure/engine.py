from intelligence.technical.engines.market_structure.structure_watch import (
    StructureWatch,
)
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from intelligence.technical.contracts import EngineBias, MarketRegime, TechnicalSignal
from intelligence.technical.data_access import TechnicalDataPlatform
from intelligence.technical.engines.market_structure.pullback_analyzer import (
    calculate_pullback_zone,
    detect_pullback,
)
from intelligence.technical.engines.market_structure.regime_classifier import (
    classify_regime,
)


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
        times = df["time"].values
        lookback = self.config["swing_lookback"]
        swings = []

        for i in range(lookback, len(df) - lookback):
            if highs[i] == max(highs[i - lookback : i + lookback + 1]):
                left_high = max(highs[i - lookback : i])
                right_high = max(highs[i + 1 : i + lookback + 1])
                if highs[i] > left_high and highs[i] > right_high:
                    strength = self._calc_strength(df, i, "high")
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

    # ---------- MTF METHOD ----------
    def analyze_mtf(
        self, symbol: str, timeframes: list[str] = None, lookback_bars: int = 200
    ) -> dict:
        if timeframes is None:
            timeframes = ["D1", "H4", "H1", "M15"]

        from datetime import datetime

        from intelligence.technical.engines.market_structure.mtf_aggregator import (
            MTFAggregator,
        )
        from intelligence.technical.engines.market_structure.swing_hierarchy import (
            classify_swings,
        )

        aggregator = MTFAggregator(self)
        aggregated = aggregator.aggregate(symbol, timeframes, lookback_bars)

        # ---- 1. Regime classification per timeframe ----
        timeframe_regimes = {}
        for tf, signal in aggregated["signals"].items():
            df = self.data.get_last_bars(symbol, tf, lookback_bars)
            swings = signal.extras.get("swings", [])
            regime_info = classify_regime(df, swings)
            timeframe_regimes[tf] = regime_info

        # ---- 2. Determine Macro, Context, Execution biases ----
        def get_bias(tf):
            sig = aggregated["signals"].get(tf)
            return sig.bias.value if sig else None

        macro_bias = get_bias("D1")
        context_bias = get_bias("H4")
        exec_bias = get_bias("H1") or get_bias("M15")

        # ---- 3. Weighted confidence ----
        weights = {"D1": 0.4, "H4": 0.3, "H1": 0.2, "M15": 0.1}
        weighted_conf = 0.0
        for tf, w in weights.items():
            sig = aggregated["signals"].get(tf)
            if sig:
                weighted_conf += sig.confidence * w
        weighted_conf = round(min(1.0, weighted_conf), 3)

        # ---- 4. Alignment classification ----
        all_biases = [get_bias(tf) for tf in timeframes if get_bias(tf)]
        all_same = len(set(all_biases)) == 1

        regime_values = []
        for tf in timeframes:
            if tf in timeframe_regimes:
                r = timeframe_regimes[tf].get("regime")
                if r:
                    regime_values.append(r.value if hasattr(r, "value") else r)
        trending_count = sum(
            1 for r in regime_values if r in ["trending_up", "trending_down"]
        )
        ranging_count = sum(1 for r in regime_values if r == "ranging")

        if all_same and trending_count == len(timeframes):
            alignment_state = "fully_aligned"
        elif all_same and ranging_count > 0:
            alignment_state = "aligned_with_consolidation"
        elif macro_bias == "bullish" and exec_bias == "bearish":
            alignment_state = "bullish_pullback"
        elif macro_bias == "bearish" and exec_bias == "bullish":
            alignment_state = "bearish_pullback"
        elif (
            macro_bias == "bearish"
            and context_bias == "bullish"
            and exec_bias == "bullish"
        ):
            alignment_state = "counter_trend_rally"
        elif (
            macro_bias == "bullish"
            and context_bias == "bearish"
            and exec_bias == "bearish"
        ):
            alignment_state = "counter_trend_decline"
        else:
            alignment_state = "divergent"

        # ---- 5. Structural interpretation ----
        interpretation = self._interpret_mtf(
            macro_bias, context_bias, exec_bias, alignment_state
        )

        # ---- 6. Pullback detection ----
        mtf_structure = {
            "timeframes": {
                tf: {"bias": sig.bias.value}
                for tf, sig in aggregated["signals"].items()
            },
            "primary_bias": aggregated["primary_bias"].value,
        }
        pullback = detect_pullback(mtf_structure)

        pullback_zone = None
        if pullback:
            primary_df = self.data.get_last_bars(symbol, "D1", 100)
            if not primary_df.empty:
                # ---- CORRECT TRUE RANGE ATR ----
                high = primary_df["high"]
                low = primary_df["low"]
                close = primary_df["close"].shift(1)
                tr1 = high - low
                tr2 = (high - close).abs()
                tr3 = (low - close).abs()
                tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
                atr = tr.rolling(14).mean().iloc[-1]
                current_price = primary_df["close"].iloc[-1]
                pullback_zone = calculate_pullback_zone(
                    primary_df, atr, current_price, aggregated["primary_bias"].value
                )

        # ---- 7. Swing hierarchy ----
        swing_hierarchy = {}
        for tf, signal in aggregated["signals"].items():
            swings = signal.extras.get("swings", [])
            swing_hierarchy[tf] = classify_swings(swings, tf)

        # ---- 8. Build final result ----
        result = {
            "symbol": symbol,
            "timestamp": datetime.now(),
            "macro_bias": macro_bias,
            "context_bias": context_bias,
            "execution_bias": exec_bias,
            "primary_bias": aggregated["primary_bias"].value,
            "alignment_state": alignment_state,
            "alignment": "aligned" if aggregated["aligned"] else "divergent",
            "weighted_confidence": weighted_conf,
            "timeframes": {
                tf: {
                    "bias": sig.bias.value,
                    "confidence": sig.confidence,
                    "regime": sig.regime.value,
                    "phase": timeframe_regimes[tf].get("phase", "unknown"),
                    "regime_confidence": timeframe_regimes[tf].get("confidence", 0.0),
                }
                for tf, sig in aggregated["signals"].items()
            },
            "swing_hierarchy": swing_hierarchy,
            "events": {tf: sig.events for tf, sig in aggregated["signals"].items()},
            "pullback": pullback,
            "pullback_zone": pullback_zone,
            "interpretation": interpretation,
        }
        return result

    def _interpret_mtf(self, macro_bias, context_bias, exec_bias, alignment_state):
        """Generate human-readable interpretation."""
        lines = []
        if alignment_state == "fully_aligned":
            lines.append(
                f"Strong {macro_bias.upper()} alignment across all timeframes."
            )
            lines.append("All timeframes confirm the same directional bias.")
            lines.append("Continuation expected.")
        elif alignment_state == "aligned_with_consolidation":
            lines.append(
                f"{macro_bias.upper()} structural alignment with short-term consolidation."
            )
            lines.append(
                "Higher timeframes are trending; lower timeframes are ranging."
            )
            lines.append("Expect continuation after consolidation.")
        elif alignment_state == "bullish_pullback":
            lines.append(
                f"{macro_bias.upper()} macro structure, bearish short-term pullback."
            )
            lines.append(
                "The current decline is likely a correction within a larger uptrend."
            )
            lines.append("Look for bullish reversal signals in lower timeframes.")
        elif alignment_state == "bearish_pullback":
            lines.append(
                f"{macro_bias.upper()} macro structure, bullish short-term recovery."
            )
            lines.append(
                "The current rally is likely a correction within a larger downtrend."
            )
            lines.append("Look for bearish reversal signals in lower timeframes.")
        elif alignment_state == "counter_trend_rally":
            lines.append(
                f"{macro_bias.upper()} macro structure, bullish counter-trend rally."
            )
            lines.append("The H4 and lower timeframes are recovering upward.")
            lines.append(
                "This is a counter-trend move; macro reversal is not confirmed."
            )
        elif alignment_state == "counter_trend_decline":
            lines.append(
                f"{macro_bias.upper()} macro structure, bearish counter-trend decline."
            )
            lines.append(
                "The H4 and lower timeframes are declining against the macro trend."
            )
            lines.append(
                "This is a counter-trend move; macro reversal is not confirmed."
            )
        else:
            lines.append("Mixed signals across timeframes.")
            lines.append("No clear consensus; exercise caution.")
        return "\n".join(lines)

    # ---------- STRUCTURE WATCH ----------
    def watch(
        self, symbol: str, timeframes: list[str] = None, lookback_bars: int = 200
    ) -> "StructureWatch":
        """
        Generate a structured watch object that includes conditions, status, and zones.
        """
        from intelligence.technical.engines.market_structure.structure_watch import (
            generate_structure_watch,
        )

        mtf_result = self.analyze_mtf(symbol, timeframes, lookback_bars)
        watch = generate_structure_watch(symbol, mtf_result)
        return watch
        try:
            # Try D1 first, then H1
            df = self.data.get_last_bars(symbol, "D1", 1)
            if df.empty:
                df = self.data.get_last_bars(symbol, "H1", 1)
            if not df.empty:
                current_price = df["close"].iloc[-1]
        except Exception:
            pass

        mtf_result = self.analyze_mtf(symbol, timeframes, lookback_bars)
        # Add current_price to mtf_result for use in watch generator
        mtf_result["current_price"] = current_price
        watch = generate_structure_watch(symbol, mtf_result, current_price)
        return watch

    def get_atr(
        self, symbol: str, period: int = 14, fallback_timeframes: list = None
    ) -> float:
        """
        Get ATR by trying multiple timeframes in order.
        """
        if fallback_timeframes is None:
            fallback_timeframes = ["M15", "H1", "H4", "D1"]
        for tf in fallback_timeframes:
            try:
                df = self.data.get_last_bars(symbol, tf, period + 10)
                if len(df) > period:
                    high = df["high"]
                    low = df["low"]
                    close = df["close"].shift(1)
                    tr1 = high - low
                    tr2 = (high - close).abs()
                    tr3 = (low - close).abs()
                    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
                    atr = tr.rolling(period).mean().iloc[-1]
                    if atr is not None and atr > 0:
                        return atr
            except Exception:
                continue
        return None
