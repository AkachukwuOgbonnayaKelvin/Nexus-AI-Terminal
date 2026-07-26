#!/usr/bin/env python
"""
Market Structure Engine – Full Certification
Tests all symbols and timeframes present in the technical store.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

from sqlalchemy import create_engine, text

from intelligence.technical.data_access import TechnicalDataPlatform
from intelligence.technical.engines.market_structure.engine import MarketStructureEngine
from intelligence.technical.stores.microstructure.repository import (
    PostgresMicrostructureRepository,
)
from intelligence.technical.stores.ohlc.repository import PostgresOHLCRepository

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"


def get_all_symbol_timeframes():
    """Fetch all distinct (symbol, timeframe) from technical_ohlc.bars."""
    engine = create_engine(DB_CONN)
    query = text("""
        SELECT DISTINCT symbol, timeframe
        FROM technical_ohlc.bars
        ORDER BY symbol, timeframe
    """)
    with engine.connect() as conn:
        result = conn.execute(query).fetchall()
    return [(row.symbol, row.timeframe) for row in result]


def run_single_test(engine, symbol, timeframe, lookback=300):
    """Run engine on one (symbol, timeframe) and return result dict."""
    signal = engine.analyze(symbol, timeframe, lookback_bars=lookback)
    bars = signal.extras.get("bars_analyzed", 0)
    swings = len(signal.extras.get("swings", []))
    bias = signal.bias.value
    regime = signal.regime.value
    confidence = signal.confidence
    data_status = signal.extras.get("data_status", "OK")
    reason = signal.reasoning[0] if signal.reasoning else None

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "bars": bars,
        "swings": swings,
        "bias": bias,
        "regime": regime,
        "confidence": round(confidence, 3),
        "data_status": data_status,
        "reason": reason,
        "passed": (bars >= 50 and swings >= 4 and bias != "unknown"),
    }


def main():
    print("\n" + "=" * 90)
    print("MARKET STRUCTURE ENGINE – FULL CERTIFICATION")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)

    # Setup
    ohlc = PostgresOHLCRepository(DB_CONN)
    micro = PostgresMicrostructureRepository(DB_CONN)
    platform = TechnicalDataPlatform(ohlc, micro)
    engine = MarketStructureEngine(platform)

    # Get all symbol/timeframe combinations
    pairs = get_all_symbol_timeframes()
    print(f"\nFound {len(pairs)} (symbol, timeframe) combinations.")

    if not pairs:
        print("❌ No data found in technical_ohlc.bars – aborting.")
        return

    # Run tests
    results = []
    for idx, (symbol, tf) in enumerate(pairs, 1):
        print(f"\rTesting {idx}/{len(pairs)}: {symbol} {tf} ...", end="", flush=True)
        res = run_single_test(engine, symbol, tf, lookback=300)
        results.append(res)

    print("\n")  # newline after progress

    # Summarize
    passed = [r for r in results if r["passed"]]
    failed = [
        r for r in results if not r["passed"] and r["data_status"] != "UNAVAILABLE"
    ]
    skipped = [r for r in results if r["data_status"] == "UNAVAILABLE"]

    print("\n" + "-" * 90)
    print(
        f"SUMMARY:  Passed: {len(passed)} | Failed: {len(failed)} | Skipped (no data): {len(skipped)}"
    )
    print("-" * 90)

    # Show passed
    if passed:
        print("\n✅ PASSED:")
        for r in passed[:10]:  # show first 10 to avoid flooding
            print(
                f"  {r['symbol']:12} {r['timeframe']:4}  bars={r['bars']:4}  swings={r['swings']:2}  bias={r['bias']:8}  conf={r['confidence']:.3f}"
            )
        if len(passed) > 10:
            print(f"  ... and {len(passed) - 10} more passed.")

    # Show failed
    if failed:
        print("\n❌ FAILED:")
        for r in failed:
            print(
                f"  {r['symbol']:12} {r['timeframe']:4}  bars={r['bars']:4}  swings={r['swings']:2}  bias={r['bias']:8}  reason='{r['reason']}'"
            )

    # Show skipped
    if skipped:
        print("\n⏭️ SKIPPED (no data):")
        for r in skipped[:10]:
            print(f"  {r['symbol']:12} {r['timeframe']:4}  {r['reason']}")
        if len(skipped) > 10:
            print(f"  ... and {len(skipped) - 10} more skipped.")

    print("\n" + "=" * 90)
    if failed:
        print("❌ CERTIFICATION FAILED – fix issues before proceeding.")
    elif skipped:
        print("⚠️ CERTIFICATION PARTIAL – some data missing, but no critical failures.")
    else:
        print("✅ CERTIFICATION PASSED – all tested combinations are healthy.")
    print("=" * 90)


if __name__ == "__main__":
    main()
