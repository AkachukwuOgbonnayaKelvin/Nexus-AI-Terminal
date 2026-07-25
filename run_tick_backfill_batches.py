#!/usr/bin/env python3
"""
Batch tick backfill runner.
Splits symbols into batches to avoid system hangs.
Aggregates ticks to M5, M15, H1, H4, D1.
"""

import os
import subprocess
import sys
import tempfile
import time

# All symbols from the original script
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

BATCH_SIZE = 5
# All five timeframes needed for Technical Intelligence
TIMEFRAMES = ["MINUTE_5", "MINUTE_15", "HOUR_1", "HOUR_4", "DAY_1"]
LOOKBACK = 90  # 3 months


def create_batch_script(batch_symbols, batch_index):
    symbols_str = repr(batch_symbols)
    timeframes_str = repr(TIMEFRAMES)
    script_content = f"""import sys
import os
sys.path.insert(0, os.getcwd())

# Override symbols and timeframes
import intelligence.data.tick.tests.run_tick_backfill as orig
from intelligence.data.volume.contracts import Timeframe

# Convert timeframe string names to Timeframe enum members
orig.SYMBOLS = {symbols_str}
orig.TIMEFRAMES = [getattr(Timeframe, tf) for tf in {timeframes_str}]

if hasattr(orig, 'LOOKBACK'):
    orig.LOOKBACK = {LOOKBACK}

# Run the backfill function
if hasattr(orig, 'run_tick_backfill'):
    orig.run_tick_backfill()
else:
    import runpy
    runpy.run_module('intelligence.data.tick.tests.run_tick_backfill', run_name='__main__', alter_sys=True)
"""

    fd, path = tempfile.mkstemp(
        suffix=".py", prefix=f"tick_batch_{batch_index:02d}_", text=True
    )
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(script_content)
    return path


def run_batch(batch_symbols, batch_index, total_batches):
    print("\n" + "=" * 60)
    print(f"Batch {batch_index}/{total_batches}: {len(batch_symbols)} symbols")
    print("Symbols: {}".format(", ".join(batch_symbols)))
    print("=" * 60)

    script_path = create_batch_script(batch_symbols, batch_index)
    try:
        cmd = [sys.executable, script_path]
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode != 0:
            print(f"Batch {batch_index} returned error code {result.returncode}")
        else:
            print(f"Batch {batch_index} completed successfully.")
    except Exception as e:
        print(f"Batch {batch_index} failed: {e}")
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

    if batch_index < total_batches:
        print("Pausing for 10 seconds...")
        time.sleep(10)


def main():
    batches = [SYMBOLS[i : i + BATCH_SIZE] for i in range(0, len(SYMBOLS), BATCH_SIZE)]
    total = len(batches)
    print(f"Total symbols: {len(SYMBOLS)}")
    print(f"Number of batches: {total}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Timeframes: {TIMEFRAMES}")
    print(f"Lookback: {LOOKBACK} days")

    start_time = time.time()
    for idx, batch in enumerate(batches, 1):
        run_batch(batch, idx, total)
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"All batches completed in {elapsed:.2f} seconds.")
    print("=" * 60)


if __name__ == "__main__":
    main()
