from enum import Enum


class MTFState(Enum):
    ALIGNED_BULLISH = "aligned_bullish"
    ALIGNED_BEARISH = "aligned_bearish"
    BULLISH_TREND = "bullish_trend"
    BEARISH_TREND = "bearish_trend"
    BULLISH_CONSOLIDATION = "bullish_consolidation"
    BEARISH_CONSOLIDATION = "bearish_consolidation"
    BULLISH_MACRO_PULLBACK = "bullish_macro_pullback"
    BEARISH_MACRO_PULLBACK = "bearish_macro_pullback"
    BULLISH_RECOVERY = "bullish_recovery"
    BEARISH_RECOVERY = "bearish_recovery"
    REVERSAL_RISK_BULLISH = "reversal_risk_bullish"
    REVERSAL_RISK_BEARISH = "reversal_risk_bearish"
    INSUFFICIENT_DATA = "insufficient_data"


def classify_state(timeframes: dict[str, dict]) -> dict:
    biases = {}
    for tf, info in timeframes.items():
        biases[tf] = info.get("bias", "unknown")

    available = {tf: bias for tf, bias in biases.items() if bias != "unknown"}
    if not available:
        return {
            "state": MTFState.INSUFFICIENT_DATA,
            "confidence": 0.0,
            "interpretation": "No valid timeframe data available.",
        }

    # If we have less than 3 timeframes, it's insufficient data
    if len(available) < 3:
        return {
            "state": MTFState.INSUFFICIENT_DATA,
            "confidence": 0.0,
            "interpretation": f"Only {len(available)} timeframes available; need at least 3 for MTF analysis.",
        }

    macro_bias = biases.get("D1")
    context_bias = biases.get("H4")
    structure_bias = biases.get("H1")
    exec_bias = biases.get("M15")

    all_biases = list(available.values())
    if (
        len(all_biases) == 4
        and all_biases[0] == all_biases[1] == all_biases[2] == all_biases[3]
    ):
        if all_biases[0] == "bullish":
            return {
                "state": MTFState.ALIGNED_BULLISH,
                "confidence": 0.9,
                "interpretation": "All timeframes aligned bullish.",
            }
        else:
            return {
                "state": MTFState.ALIGNED_BEARISH,
                "confidence": 0.9,
                "interpretation": "All timeframes aligned bearish.",
            }

    if macro_bias == "bullish":
        if (
            context_bias == "bullish"
            and structure_bias == "bullish"
            and exec_bias == "bullish"
        ):
            return {
                "state": MTFState.BULLISH_TREND,
                "confidence": 0.85,
                "interpretation": "Bullish trend across timeframes.",
            }
        elif (
            context_bias == "bullish"
            and structure_bias == "bullish"
            and exec_bias in ["ranging", "unknown"]
        ):
            return {
                "state": MTFState.BULLISH_CONSOLIDATION,
                "confidence": 0.75,
                "interpretation": "Bullish trend with short-term consolidation.",
            }
        elif (
            context_bias in ["bearish", "ranging"]
            and structure_bias in ["bearish", "ranging"]
            and exec_bias in ["bullish", "ranging"]
        ):
            return {
                "state": MTFState.BULLISH_MACRO_PULLBACK,
                "confidence": 0.7,
                "interpretation": "Bullish macro structure with bearish pullback/correction.",
            }
        elif (
            context_bias in ["bullish", "ranging"]
            and structure_bias in ["bearish", "ranging"]
            and exec_bias == "bullish"
        ):
            return {
                "state": MTFState.BULLISH_RECOVERY,
                "confidence": 0.65,
                "interpretation": "Bullish recovery within a pullback.",
            }
        else:
            return {
                "state": MTFState.REVERSAL_RISK_BULLISH,
                "confidence": 0.5,
                "interpretation": "Mixed signals; reversal risk to the downside.",
            }

    elif macro_bias == "bearish":
        if (
            context_bias == "bearish"
            and structure_bias == "bearish"
            and exec_bias == "bearish"
        ):
            return {
                "state": MTFState.BEARISH_TREND,
                "confidence": 0.85,
                "interpretation": "Bearish trend across timeframes.",
            }
        elif (
            context_bias == "bearish"
            and structure_bias == "bearish"
            and exec_bias in ["ranging", "unknown"]
        ):
            return {
                "state": MTFState.BEARISH_CONSOLIDATION,
                "confidence": 0.75,
                "interpretation": "Bearish trend with short-term consolidation.",
            }
        elif (
            context_bias in ["bullish", "ranging"]
            and structure_bias in ["bullish", "ranging"]
            and exec_bias in ["bearish", "ranging"]
        ):
            return {
                "state": MTFState.BEARISH_MACRO_PULLBACK,
                "confidence": 0.7,
                "interpretation": "Bearish macro structure with bullish pullback/recovery.",
            }
        elif (
            context_bias in ["bearish", "ranging"]
            and structure_bias in ["bullish", "ranging"]
            and exec_bias == "bearish"
        ):
            return {
                "state": MTFState.BEARISH_RECOVERY,
                "confidence": 0.65,
                "interpretation": "Bearish recovery within a pullback.",
            }
        else:
            return {
                "state": MTFState.REVERSAL_RISK_BEARISH,
                "confidence": 0.5,
                "interpretation": "Mixed signals; reversal risk to the upside.",
            }

    else:
        if (
            context_bias == "bullish"
            and structure_bias == "bullish"
            and exec_bias == "bullish"
        ):
            return {
                "state": MTFState.BULLISH_TREND,
                "confidence": 0.7,
                "interpretation": "Bullish intermediate trend (macro data missing).",
            }
        elif (
            context_bias == "bearish"
            and structure_bias == "bearish"
            and exec_bias == "bearish"
        ):
            return {
                "state": MTFState.BEARISH_TREND,
                "confidence": 0.7,
                "interpretation": "Bearish intermediate trend (macro data missing).",
            }
        else:
            return {
                "state": MTFState.INSUFFICIENT_DATA,
                "confidence": 0.0,
                "interpretation": "Insufficient or conflicting data.",
            }
