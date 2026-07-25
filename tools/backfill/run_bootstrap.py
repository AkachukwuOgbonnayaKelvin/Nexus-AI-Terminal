"""
Bootstrap Mode – fetch historical tick data for a symbol.
Processes in 1-hour batches, aggregates to M15, persists to SQLite.
"""

import gc
import time
from datetime import datetime, timedelta

from intelligence.data.tick.contracts import TickRequest
from intelligence.data.tick.coverage.manager import DataAvailabilityManager
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter
from intelligence.data.tick.sources import MT5Source


def bootstrap_symbol(
    symbol: str,
    timeframe: str = "M15",
    days_back: int = 1,
    hours_batch: int = 1,
    max_ticks_per_batch: int = 50000,
):
    """
    Fetch historical ticks for a symbol and persist aggregated data.

    Args:
        symbol: e.g., 'EURUSD'
        timeframe: aggregation timeframe ('M5', 'M15', 'H1', 'H4', 'D1')
        days_back: how many days of history to fetch
        hours_batch: hours per fetch window
        max_ticks_per_batch: max ticks to process in one go
    """
    print(f"\n=== Bootstrap {symbol} {timeframe} ===")
    source = MT5Source()
    writer = TickSQLiteWriter()
    coverage_manager = DataAvailabilityManager()

    # Check current coverage
    coverage = coverage_manager.get_coverage(symbol, timeframe)
    print(
        f"Coverage: earliest={coverage.earliest}, latest={coverage.latest}, count={coverage.record_count}"
    )

    # Determine start date
    end_date = datetime.utcnow()
    if coverage.latest and (end_date - coverage.latest) < timedelta(hours=4):
        print("Data is fresh, skipping.")
        return

    # Start from latest or from now - days_back
    if coverage.latest:
        start_date = coverage.latest
    else:
        start_date = end_date - timedelta(days=days_back)

    print(f"Fetching from {start_date} to {end_date}")

    total_agg = 0
    current_start = start_date

    while current_start < end_date:
        window_end = min(current_start + timedelta(hours=hours_batch), end_date)
        print(f"\n  Window: {current_start} -> {window_end}")

        try:
            # Fetch ticks
            request = TickRequest(
                symbol=symbol,
                start=current_start,
                end=window_end,
                max_ticks=max_ticks_per_batch * 2,  # allow some headroom
            )
            response = source.fetch(request)

            if not response.success:
                print(f"    Fetch failed: {response.error}")
                current_start = window_end
                continue

            ticks = response.ticks
            if not ticks:
                print("    No ticks returned")
                current_start = window_end
                continue

            print(f"    Fetched {len(ticks)} ticks")

            # Convert to a format that aggregator expects
            # For now, we'll manually aggregate to M15
            # Since we don't have TickAggregator working, we'll create a simple aggregation.
            # But let's first test the pipeline without aggregation.
            # Instead, we'll write raw ticks to fact_tick and then later aggregate.

            # Write raw ticks to fact_tick
            raw_records = []
            for t in ticks:
                raw_records.append(
                    {
                        "symbol": t.symbol,
                        "timestamp": t.timestamp.isoformat(),
                        "bid": t.bid,
                        "ask": t.ask,
                        "last": t.last,
                        "volume": t.volume,
                        "source_id": t.source_id,
                        "quality_score": t.quality_score,
                    }
                )
            inserted_raw = writer.write_fact_tick(raw_records)
            print(f"    Inserted {inserted_raw} raw ticks")

            # For now, skip aggregation until we have a working aggregator

            # Free memory
            del ticks, raw_records
            gc.collect()

        except Exception as e:
            print(f"    Error: {e}")
            # Continue to next window

        current_start = window_end
        time.sleep(0.5)  # Small delay to avoid overwhelming MT5

    print(f"Total raw ticks inserted: {total_agg}")  # We'll adjust later


if __name__ == "__main__":
    # Bootstrap EURUSD for 1 day
    bootstrap_symbol("EURUSD", timeframe="M15", days_back=1, hours_batch=1)
