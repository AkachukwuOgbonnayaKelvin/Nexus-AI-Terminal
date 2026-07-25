import gc
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

# Imports from tick engine
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
SYMBOLS = ["EURUSD"]  # Start with one symbol
TIMEFRAMES = [Timeframe.MINUTE_15]  # Start with one timeframe
WINDOW_HOURS = 1  # Process 1 hour at a time
MAX_TICKS_PER_BATCH = 20000  # Process in chunks of 20k ticks
DAYS_BACK = 1  # Start with 1 day
CHECKPOINT_FILE = "./data/tick_backfill_safe_checkpoint.json"


def get_checkpoint() -> dict:
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    return {"completed": []}  # list of (symbol, timeframe, end_time)


def save_checkpoint(checkpoint: dict):
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f, indent=2)


def process_symbol_timeframe(
    symbol: str, timeframe: Timeframe, start_date: datetime, end_date: datetime
):
    print(
        f"\n=== Processing {symbol} {timeframe.value} from {start_date} to {end_date} ==="
    )
    writer = TickSQLiteWriter()
    checkpoint = get_checkpoint()

    # Check if already completed
    completed_key = f"{symbol}_{timeframe.value}_{end_date.isoformat()}"
    if completed_key in checkpoint.get("completed", []):
        print("  Skipping (already completed)")
        return 0

    # Setup components
    sources = get_default_tick_sources()
    router = TickSourceRouter(sources)
    executor = TickAcquisitionExecutor(router)
    validator = RawTickValidator()
    classifier = TickClassifier()
    aggregator = TickAggregator()
    quality = TickQualityEngine()

    total_aggregated = 0
    current_start = start_date

    while current_start < end_date:
        window_end = min(current_start + timedelta(hours=WINDOW_HOURS), end_date)
        print(f"\n  Window: {current_start} to {window_end}")

        try:
            # Fetch ticks for this window
            ticks = executor.fetch_ticks(symbol, current_start, window_end)
            if not ticks:
                print("    No ticks fetched")
                current_start = window_end
                continue

            print(f"    Fetched {len(ticks)} ticks")

            # Process in smaller batches
            total_batch_agg = 0
            for i in range(0, len(ticks), MAX_TICKS_PER_BATCH):
                batch = ticks[i : i + MAX_TICKS_PER_BATCH]
                print(f"      Batch {i // MAX_TICKS_PER_BATCH + 1}: {len(batch)} ticks")

                # Validate
                valid = validator.validate_batch(batch)
                if not valid:
                    print("        No valid ticks")
                    continue

                # Classify
                classified = classifier.classify_batch(valid)
                if not classified:
                    print("        No classified ticks")
                    continue

                # Aggregate
                aggregated = aggregator.aggregate_batch(classified, timeframe)
                if not aggregated:
                    print("        No aggregated records")
                    continue

                # Quality
                quality_scores = quality.assess_batch(aggregated)

                # Persist
                inserted_agg = writer.write_fact_aggregated(aggregated)
                total_aggregated += inserted_agg
                total_batch_agg += inserted_agg
                print(f"        Inserted {inserted_agg} aggregated records")

                # Clear memory
                del batch, valid, classified, aggregated, quality_scores
                gc.collect()

            print(f"    Window inserted {total_batch_agg} aggregated records")

        except Exception as e:
            print(f"    Error in window: {e}")
            # Save checkpoint and exit so we can resume later
            checkpoint["completed"].append(completed_key)
            save_checkpoint(checkpoint)
            raise

        # Update checkpoint
        checkpoint["last_processed"] = {
            "symbol": symbol,
            "timeframe": timeframe.value,
            "window_end": window_end.isoformat(),
        }
        save_checkpoint(checkpoint)

        current_start = window_end

    # Mark as completed
    checkpoint["completed"].append(completed_key)
    save_checkpoint(checkpoint)
    print(
        f"  Completed {symbol} {timeframe.value}. Total aggregated: {total_aggregated}"
    )
    return total_aggregated


def main():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=DAYS_BACK)

    print("Starting safe tick backfill")
    print(f"Symbols: {SYMBOLS}")
    print(f"Timeframes: {[t.value for t in TIMEFRAMES]}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Window size: {WINDOW_HOURS} hour(s)")
    print(f"Max ticks per batch: {MAX_TICKS_PER_BATCH}")

    total = 0
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            inserted = process_symbol_timeframe(symbol, tf, start_date, end_date)
            total += inserted

    print(f"\n✅ Total aggregated records inserted: {total}")


if __name__ == "__main__":
    main()
