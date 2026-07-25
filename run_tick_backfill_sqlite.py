import gc
import os
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

from intelligence.data.tick.acquisition.executor import TickAcquisitionExecutor
from intelligence.data.tick.aggregation import TickAggregator
from intelligence.data.tick.classification import TickClassifier
from intelligence.data.tick.contracts import Timeframe
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter
from intelligence.data.tick.quality import TickQualityEngine
from intelligence.data.tick.registry import get_default_tick_sources
from intelligence.data.tick.routing import TickSourceRouter
from intelligence.data.tick.validation import RawTickValidator

# Configuration
SYMBOLS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCHF",
    "USDCAD",
    "NZDUSD",
    "EURGBP",
    "EURJPY",
    "GBPJPY",
    "AUDJPY",
    "GBPAUD",
    "XAUUSD",
    "XAGUSD",
    "US500",
    "US100",
    "US30",
    "GER40",
    "UK100",
    "JP225",
    "HK50",
    "AU200",
    "CHINA50",
    "FRA40",
    "CL=F",
    "BZ=F",
    "NG=F",
    "COPPER",
    "PLATINUM",
    "PALLADIUM",
    "ALUMINUM",
    "US02Y",
    "US10Y",
    "US30Y",
    "DE10Y",
    "GB10Y",
    "JP10Y",
    "BTCUSD",
    "ETHUSD",
    "SOLUSD",
    "ADAUSD",
    "DOTUSD",
    "LINKUSD",
]

TIMEFRAMES = [
    Timeframe.MINUTE_1,
    Timeframe.MINUTE_5,
    Timeframe.MINUTE_15,
    Timeframe.HOUR_1,
]

# Use a recent 3-day window for testing; change to 90 days for full backfill
DAYS_BACK = 3  # Change to 90 for full
END_DATE = datetime.utcnow()
START_DATE = END_DATE - timedelta(days=DAYS_BACK)


def process_symbol_timeframe(symbol, timeframe):
    print(f"\n=== Processing {symbol} {timeframe.value} ===")
    writer = TickSQLiteWriter()

    # Check if already complete
    latest = writer.get_latest_timestamp(symbol, timeframe.value)
    if latest:
        print(f"  Latest aggregated timestamp: {latest}")
        # If latest is close to END_DATE, skip
        latest_dt = datetime.fromisoformat(latest)
        if (END_DATE - latest_dt).total_seconds() < 3600:
            print("  Data is recent, skipping")
            return

    # Setup components
    sources = get_default_tick_sources()
    router = TickSourceRouter(sources)
    executor = TickAcquisitionExecutor(router)
    validator = RawTickValidator()
    classifier = TickClassifier()
    aggregator = TickAggregator()
    quality = TickQualityEngine()

    # Fetch in chunks (1-hour batches)
    current_start = START_DATE
    total_inserted = 0
    batch = 0

    while current_start < END_DATE:
        batch_end = min(current_start + timedelta(hours=1), END_DATE)
        print(f"  Batch {batch + 1}: {current_start} to {batch_end}")

        try:
            ticks = executor.fetch_ticks(symbol, current_start, batch_end)
            if not ticks:
                print("    No ticks")
                current_start = batch_end
                batch += 1
                continue

            valid = validator.validate(ticks)
            classified = classifier.classify(valid)
            aggregated = aggregator.aggregate(classified, timeframe)
            quality_scores = quality.assess(aggregated)

            # Write to SQLite
            inserted = writer.write_aggregated(
                aggregated, source_id=f"backfill_{symbol}"
            )
            total_inserted += inserted
            print(f"    Inserted {inserted} aggregated records")

            # Clear memory
            del ticks, valid, classified, aggregated, quality_scores
            gc.collect()

            time.sleep(0.5)  # brief pause to avoid overloading

        except Exception as e:
            print(f"    Error: {e}")
            # Continue to next batch

        current_start = batch_end
        batch += 1

    print(f"  Total aggregated inserted: {total_inserted}")
    return total_inserted


def run_all():
    total_symbols = len(SYMBOLS)
    total_timeframes = len(TIMEFRAMES)
    print(f"Processing {total_symbols} symbols × {total_timeframes} timeframes")
    print(f"Date range: {START_DATE} to {END_DATE}")

    overall_total = 0
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            inserted = process_symbol_timeframe(symbol, tf)
            overall_total += inserted

    print(f"\n✅ Total aggregated records inserted: {overall_total}")


if __name__ == "__main__":
    run_all()
