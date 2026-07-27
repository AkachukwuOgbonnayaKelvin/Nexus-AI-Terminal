import hashlib
from dataclasses import dataclass, field
from enum import Enum


class WatchStatus(Enum):
    ANALYZING = "analyzing"
    WAITING = "waiting"
    APPROACHING_ZONE = "approaching_zone"
    IN_ZONE = "in_zone"
    CONFIRMATION_PENDING = "confirmation_pending"
    CONDITION_MET = "condition_met"
    CONFIRMED = "confirmed"
    INVALIDATED = "invalidated"
    EXPIRED = "expired"
    DATA_ERROR = "data_error"
    PROJECTION_INVALID = "projection_invalid"


class MarketState(Enum):
    TREND_CONTINUATION = "trend_continuation"
    CONSOLIDATION_BEFORE_CONTINUATION = "consolidation_before_continuation"
    PULLBACK_EXPECTED = "pullback_expected"
    PULLBACK_APPROACHING = "pullback_approaching"
    PULLBACK_IN_PROGRESS = "pullback_in_progress"
    PULLBACK_ZONE_REACHED = "pullback_zone_reached"
    REVERSAL_CONFIRMATION_PENDING = "reversal_confirmation_pending"
    BREAKOUT_PENDING = "breakout_pending"
    BREAKOUT_CONFIRMED = "breakout_confirmed"
    RANGE_ROTATION = "range_rotation"
    DISTRIBUTION = "distribution"
    ACCUMULATION = "accumulation"
    REVERSAL_RISK = "reversal_risk"
    NO_TRADE = "no_trade"


@dataclass
class Condition:
    code: str
    label: str
    met: bool = False
    required: bool = True


@dataclass
class StructureWatch:
    symbol: str
    macro_bias: str
    context_bias: str
    execution_bias: str
    market_state: MarketState

    pullback_expected: bool
    pullback_zone_low: float | None = None
    pullback_zone_high: float | None = None
    atr_value: float | None = None
    expected_pullback_atr: float | None = None
    expected_duration_min: int | None = None
    expected_duration_max: int | None = None

    current_price: float | None = None
    zone_status: str | None = None
    distance_to_zone: float | None = None
    distance_atr: float | None = None
    time_to_zone_min: float | None = None
    time_to_zone_max: float | None = None

    conditions: list[Condition] = field(default_factory=list)
    invalidation_level: float | None = None
    confidence: float = 0.0
    status: WatchStatus = WatchStatus.WAITING
    interpretation: str = ""

    setup_id: str | None = None
    notification_sent: bool = False

    projection_valid: bool = True
    validation_errors: list[str] = field(default_factory=list)


def generate_structure_watch(
    symbol: str, mtf_result: dict, current_price: float = None, atr: float = None
) -> StructureWatch:
    macro_bias = mtf_result.get("macro_bias", "neutral")
    context_bias = mtf_result.get("context_bias", "neutral")
    exec_bias = mtf_result.get("execution_bias", "neutral")
    alignment_state = mtf_result.get("alignment_state", "divergent")
    weighted_conf = mtf_result.get("weighted_confidence", 0.5)
    pullback_info = mtf_result.get("pullback")
    pullback_expected = pullback_info is not None and pullback_info.get("active", False)

    # Use provided ATR or fallback
    atr_val = atr if atr else mtf_result.get("fallback_atr")
    if atr_val is None:
        atr_val = mtf_result.get("pullback_zone", {}).get("atr_value")

    # ---- Determine market state ----
    if alignment_state == "fully_aligned":
        market_state = MarketState.TREND_CONTINUATION
    elif alignment_state == "aligned_with_consolidation":
        market_state = MarketState.CONSOLIDATION_BEFORE_CONTINUATION
    elif alignment_state in ["bullish_pullback", "bearish_pullback"]:
        if pullback_expected and atr_val and current_price:
            # Estimate zone from swing levels or fallback to ATR
            zone_low, zone_high = calculate_multi_factor_zone(
                mtf_result, current_price, atr_val, macro_bias
            )
            if zone_low and zone_high:
                if current_price < zone_low or current_price > zone_high:
                    market_state = MarketState.PULLBACK_APPROACHING
                else:
                    market_state = MarketState.PULLBACK_IN_PROGRESS
            else:
                market_state = MarketState.PULLBACK_EXPECTED
        else:
            market_state = MarketState.PULLBACK_EXPECTED
    elif alignment_state in ["counter_trend_rally", "counter_trend_decline"]:
        market_state = MarketState.REVERSAL_RISK
    else:
        market_state = MarketState.NO_TRADE

    # ---- Build zone from multi-factor or ATR ----
    zone_low, zone_high = None, None
    if pullback_expected and atr_val and current_price:
        zone_low, zone_high = calculate_multi_factor_zone(
            mtf_result, current_price, atr_val, macro_bias
        )

    # ---- Current price, zone status, distance ----
    zone_status = None
    distance_to_zone = None
    distance_atr = None
    if zone_low is not None and zone_high is not None and current_price is not None:
        if current_price < zone_low:
            zone_status = "below"
            distance_to_zone = zone_low - current_price
        elif current_price > zone_high:
            zone_status = "above"
            distance_to_zone = current_price - zone_high
        else:
            zone_status = "inside"
            distance_to_zone = 0.0
        if atr_val and atr_val > 0:
            distance_atr = distance_to_zone / atr_val
        else:
            distance_atr = 0.0

    # ---- Time to zone ----
    time_to_zone_min = time_to_zone_max = None
    if zone_low and zone_high and current_price and atr_val and atr_val > 0:
        from intelligence.technical.engines.market_structure.pullback_analyzer import (
            estimate_time_to_zone,
        )

        time_info = estimate_time_to_zone(
            current_price, zone_low, zone_high, atr_val, "H1"
        )
        if time_info.get("hours_min") is not None:
            time_to_zone_min = time_info["hours_min"]
            time_to_zone_max = time_info["hours_max"]

    # ---- Expected duration ----
    if pullback_expected and zone_low is not None and zone_high is not None:
        dur_min, dur_max = 3, 6
    else:
        dur_min, dur_max = None, None

    # ---- Build conditions with deduplication ----
    condition_dict = {}

    # Structure
    if macro_bias in ["bullish", "bearish"]:
        condition_dict["MACRO_STRUCTURE"] = Condition(
            code="MACRO_STRUCTURE",
            label=f"{'Bullish' if macro_bias == 'bullish' else 'Bearish'} structure confirmed",
            met=True,
            required=True,
        )
    else:
        condition_dict["MACRO_STRUCTURE"] = Condition(
            code="MACRO_STRUCTURE",
            label="Macro structure not confirmed",
            met=False,
            required=True,
        )

    # Volatility (ATR)
    if atr_val and atr_val > 0:
        condition_dict["ATR_AVAILABLE"] = Condition(
            code="ATR_AVAILABLE",
            label="ATR available",
            met=True,
            required=pullback_expected,
        )
    else:
        condition_dict["ATR_AVAILABLE"] = Condition(
            code="ATR_AVAILABLE",
            label="ATR not available",
            met=False,
            required=pullback_expected,
        )

    # Location (zone)
    if pullback_expected and zone_low is not None and zone_high is not None:
        in_zone = zone_status == "inside"
        condition_dict["PRICE_IN_ZONE"] = Condition(
            code="PRICE_IN_ZONE",
            label="Price inside pullback zone",
            met=in_zone,
            required=True,
        )
    else:
        condition_dict["PRICE_IN_ZONE"] = Condition(
            code="PRICE_IN_ZONE",
            label="No pullback zone active",
            met=True,
            required=False,
        )

    # Confirmation trigger
    if alignment_state in ["bullish_pullback", "bearish_pullback"]:
        condition_dict["LOWER_TF_REVERSAL"] = Condition(
            code="LOWER_TF_REVERSAL",
            label="Lower‑timeframe reversal signal (BOS/CHoCH)",
            met=False,
            required=True,
        )
    elif alignment_state == "aligned_with_consolidation":
        condition_dict["CONTINUATION_CONFIRMATION"] = Condition(
            code="CONTINUATION_CONFIRMATION",
            label="Bullish continuation confirmation (BOS/CHoCH)",
            met=False,
            required=True,
        )
    else:
        condition_dict["CONFIRMATION_PENDING"] = Condition(
            code="CONFIRMATION_PENDING",
            label="Confirmation pending",
            met=False,
            required=True,
        )

    # Invalidation (optional)
    invalidation = (
        mtf_result.get("timeframes", {}).get("D1", {}).get("invalidation_level")
    )
    if invalidation:
        condition_dict["INVALIDATION_LEVEL"] = Condition(
            code="INVALIDATION_LEVEL",
            label=f"Invalidation level: {invalidation:.5f}",
            met=True,
            required=False,
        )

    # Convert to list
    conditions = list(condition_dict.values())

    # ---- Determine status ----
    required_met = all(c.met for c in conditions if c.required)
    if not required_met:
        status = WatchStatus.WAITING
    elif pullback_expected and zone_status == "inside" and required_met:
        status = WatchStatus.CONFIRMATION_PENDING
    elif pullback_expected and zone_status in ["below", "above"] and required_met:
        status = WatchStatus.APPROACHING_ZONE
    elif pullback_expected and zone_status == "inside" and not required_met:
        status = WatchStatus.IN_ZONE
    elif macro_bias != "neutral" and alignment_state != "divergent":
        status = WatchStatus.CONFIRMATION_PENDING
    else:
        status = WatchStatus.ANALYZING

    # ---- Setup ID ----
    setup_id = None
    if zone_low is not None and zone_high is not None and macro_bias:
        data = f"{symbol}_{macro_bias}_{zone_low:.5f}_{zone_high:.5f}_{alignment_state}"
        setup_id = hashlib.md5(data.encode()).hexdigest()[:10]

    # ---- Interpretation ----
    interp = mtf_result.get("interpretation", "No interpretation available.")

    return StructureWatch(
        symbol=symbol,
        macro_bias=macro_bias,
        context_bias=context_bias,
        execution_bias=exec_bias,
        market_state=market_state,
        pullback_expected=pullback_expected,
        pullback_zone_low=zone_low,
        pullback_zone_high=zone_high,
        atr_value=atr_val,
        expected_pullback_atr=1.2 if pullback_expected else None,
        expected_duration_min=dur_min,
        expected_duration_max=dur_max,
        current_price=current_price,
        zone_status=zone_status,
        distance_to_zone=distance_to_zone,
        distance_atr=distance_atr,
        time_to_zone_min=time_to_zone_min,
        time_to_zone_max=time_to_zone_max,
        conditions=conditions,
        invalidation_level=invalidation,
        confidence=weighted_conf,
        status=status,
        interpretation=interp,
        setup_id=setup_id,
        notification_sent=False,
        projection_valid=True,
        validation_errors=[],
    )


def calculate_multi_factor_zone(
    mtf_result: dict, current_price: float, atr: float, bias: str
):
    """
    Compute pullback zone using multiple factors: structural swings, ATR, and fibonacci.
    Returns (low, high) or (None, None) if insufficient data.
    """
    swings = mtf_result.get("swing_hierarchy", {}).get("D1", [])
    if not swings:
        # Fallback to ATR-only zone
        depth = 1.2 * atr
        if bias == "bullish":
            return current_price - depth * 1.2, current_price - depth * 0.8
        else:
            return current_price + depth * 0.8, current_price + depth * 1.2

    # Get recent swing high/low
    highs = [s["price"] for s in swings if s["type"] == "high"]
    lows = [s["price"] for s in swings if s["type"] == "low"]
    if not highs or not lows:
        return None, None

    recent_high = max(highs[-3:])  # last 3 swing highs
    recent_low = min(lows[-3:])  # last 3 swing lows

    # Combine structural levels with ATR
    if bias == "bullish":
        # Zone for bullish pullback: retracement into demand
        # Use 38.2%–61.8% retracement from recent high to low
        range_ = recent_high - recent_low
        fib_38 = recent_high - range_ * 0.382
        fib_62 = recent_high - range_ * 0.618
        zone_low = min(fib_62, current_price - 1.2 * atr)
        zone_high = max(fib_38, current_price - 0.8 * atr)
    else:
        # Zone for bearish rally: retracement into supply
        range_ = recent_high - recent_low
        fib_38 = recent_low + range_ * 0.382
        fib_62 = recent_low + range_ * 0.618
        zone_low = min(fib_38, current_price + 0.8 * atr)
        zone_high = max(fib_62, current_price + 1.2 * atr)

    # Ensure zone bounds are sensible
    if zone_low > zone_high:
        zone_low, zone_high = zone_high, zone_low
    # Avoid too wide zones (cap at 2 ATR)
    if zone_high - zone_low > 2 * atr:
        mid = (zone_low + zone_high) / 2
        zone_low = mid - atr
        zone_high = mid + atr

    return zone_low, zone_high
