"""
Certification test for Technical Data Access Layer.
"""

import sys
from datetime import datetime, timedelta

from intelligence.technical import TechnicalDataAccess


def test_symbol_discovery():
    td = TechnicalDataAccess()
    symbols = td.get_symbols()
    assert len(symbols) > 0, "No symbols found"
    print(f"✅ Symbol discovery: {len(symbols)} symbols found")
    return symbols


def test_timeframe_discovery():
    td = TechnicalDataAccess()
    timeframes = td.get_timeframes()
    assert len(timeframes) > 0, "No timeframes found"
    print(f"✅ Timeframe discovery: {timeframes}")
    return timeframes


def test_ohlcv_retrieval():
    td = TechnicalDataAccess()
    df = td.get_candles("EURUSD", "D1", limit=10)
    assert not df.empty, "No data returned"
    assert "time" in df.columns, "Missing time column"
    assert "open" in df.columns, "Missing open"
    assert "high" in df.columns, "Missing high"
    assert "low" in df.columns, "Missing low"
    assert "close" in df.columns, "Missing close"
    assert "volume" in df.columns, "Missing volume"
    print(f"✅ OHLCV retrieval: {len(df)} rows")
    return df


def test_time_range():
    td = TechnicalDataAccess()
    end = datetime.now()
    start = end - timedelta(days=30)
    df = td.get_candles("EURUSD", "D1", start=start, end=end)
    assert not df.empty, "No data in time range"
    assert df["time"].min() >= start, f"Earliest timestamp {df['time'].min()} < {start}"
    assert df["time"].max() <= end, f"Latest timestamp {df['time'].max()} > {end}"
    print(f"✅ Time range: {len(df)} rows between {start.date()} and {end.date()}")


def test_limit():
    td = TechnicalDataAccess()
    df = td.get_candles("EURUSD", "D1", limit=5)
    assert len(df) <= 5, f"Limit 5 returned {len(df)} rows"
    print(f"✅ Limit: {len(df)} rows (<=5)")


def test_chronological_order():
    td = TechnicalDataAccess()
    df = td.get_candles("EURUSD", "D1", limit=50)
    times = df["time"].tolist()
    assert times == sorted(times), "Timestamps not in ascending order"
    print("✅ Chronological order: all timestamps ascending")


def test_coverage():
    td = TechnicalDataAccess()
    cov = td.get_coverage("EURUSD", "D1")
    assert cov["earliest"] is not None, "No earliest date"
    assert cov["latest"] is not None, "No latest date"
    print(f"✅ Coverage: {cov['earliest']} → {cov['latest']}")


def test_multi_timeframe():
    td = TechnicalDataAccess()
    results = td.get_multi_timeframe("USDJPY", ["D1", "H1"], limit=3)
    assert "D1" in results, "Missing D1"
    assert "H1" in results, "Missing H1"
    for tf, df in results.items():
        assert not df.empty, f"Empty DataFrame for {tf}"
    print("✅ Multi-timeframe: D1 and H1 returned")


def test_invalid_symbol():
    td = TechnicalDataAccess()
    df = td.get_candles("INVALID_SYMBOL", "D1")
    assert df.empty, "Invalid symbol should return empty DataFrame"
    print("✅ Invalid symbol: handled gracefully")


def test_invalid_timeframe():
    td = TechnicalDataAccess()
    df = td.get_candles("EURUSD", "INVALID_TF")
    assert df.empty, "Invalid timeframe should return empty DataFrame"
    print("✅ Invalid timeframe: handled gracefully")


if __name__ == "__main__":
    print("=== Technical Data Access Layer Certification ===\n")
    try:
        test_symbol_discovery()
        test_timeframe_discovery()
        test_ohlcv_retrieval()
        test_time_range()
        test_limit()
        test_chronological_order()
        test_coverage()
        test_multi_timeframe()
        test_invalid_symbol()
        test_invalid_timeframe()
        print("\n✅ ALL TESTS PASSED. Technical Data Access Layer CERTIFIED.")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
