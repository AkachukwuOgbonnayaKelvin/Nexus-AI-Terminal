#!/usr/bin/env python
"""
Run the Market Structure Engine on multiple symbols/timeframes
and display the results.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

from intelligence.technical.data_access import TechnicalDataPlatform
from intelligence.technical.engines.market_structure.engine import MarketStructureEngine
from intelligence.technical.stores.microstructure.repository import (
    PostgresMicrostructureRepository,
)
from intelligence.technical.stores.ohlc.repository import PostgresOHLCRepository

# Database connection – change if needed
DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"


def run_analysis(symbol, timeframe, lookback=300):
    """Run market structure analysis for one symbol/timeframe."""
    try:
        ohlc = PostgresOHLCRepository(DB_CONN)
        micro = PostgresMicrostructureRepository(DB_CONN)
        platform = TechnicalDataPlatform(ohlc, micro)
        engine = MarketStructureEngine(platform)

        signal = engine.analyze(symbol, timeframe, lookback_bars=lookback)

        # Count swings detected
        swing_count = len(signal.extras.get("swings", []))

        # Build result dict for pretty printing
        result = {
            "symbol": signal.symbol,
            "timeframe": signal.timeframe,
            "bias": signal.bias.value,
            "confidence": round(signal.confidence, 3),
            "regime": signal.regime.value,
            "regime_confidence": round(signal.regime_confidence, 3),
            "invalidation_level": signal.invalidation_level,
            "invalidation_condition": signal.invalidation_condition,
            "key_levels": signal.key_levels,
            "events": signal.events,
            "reasoning": signal.reasoning,
            "data_quality": round(signal.data_quality, 3),
            "bars_analyzed": signal.extras.get("bars_analyzed", 0),
            "swing_count": swing_count,
        }
        return result
    except Exception as e:
        return {"error": str(e), "symbol": symbol, "timeframe": timeframe}


def main():
    # Define test cases: (symbol, timeframe, lookback_bars)
    tests = [
        ("EURUSD", "H1", 300),
        ("EURUSD", "D1", 100),
        ("XAUUSD", "H1", 300),
        ("USDJPY", "H1", 300),
        ("AUDUSD", "D1", 100),
    ]

    print("\n" + "=" * 80)
    print("MARKET STRUCTURE ENGINE – TEST RUN")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    for symbol, tf, lookback in tests:
        print(f"\n>>> Analyzing {symbol} {tf} (lookback={lookback} bars)")
        print("-" * 50)
        result = run_analysis(symbol, tf, lookback)

        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
            continue

        print(f"  Bias:              {result['bias']}")
        print(f"  Confidence:        {result['confidence']:.2f}")
        print(
            f"  Regime:            {result['regime']} (conf: {result['regime_confidence']:.2f})"
        )
        print(f"  Data Quality:      {result['data_quality']:.2f}")
        print(f"  Bars analyzed:     {result['bars_analyzed']}")
        print(f"  Swing points:      {result['swing_count']}")
        if result["invalidation_level"]:
            print(
                f"  Invalidation:      {result['invalidation_level']:.5f} ({result['invalidation_condition']})"
            )

        if result["key_levels"]:
            print("  Key Levels:")
            for lv in result["key_levels"][:5]:
                print(
                    f"    {lv['type'].capitalize():12} {lv['level']:.5f}  strength={lv['strength']:.2f}"
                )

        if result["events"]:
            print("  Events:")
            for ev in result["events"][:3]:
                print(
                    f"    {ev['type']:15} at {ev['level']:.5f}  (significance={ev.get('significance', 0):.2f})"
                )

        if result["reasoning"]:
            print("  Reasoning:")
            for r in result["reasoning"]:
                print(f"    - {r}")

    print("\n" + "=" * 80)
    print("Test completed.")
    print("=" * 80)


if __name__ == "__main__":
    main()
