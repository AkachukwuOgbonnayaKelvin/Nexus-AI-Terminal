import os
import sys
from datetime import datetime, timedelta

import intelligence.data.tick.tests.run_tick_backfill as module

sys.path.insert(0, os.getcwd())

from intelligence.data.tick.contracts import Timeframe
from intelligence.data.tick.tests.run_tick_backfill import run_tick_backfill

# Override: test one symbol, one timeframe, 3 days
SYMBOLS = ["EURUSD"]
TIMEFRAMES = [Timeframe.MINUTE_15]
START_DATE = datetime.utcnow() - timedelta(days=3)
END_DATE = datetime.utcnow()

print("TEST MODE")
print(f"Symbols: {SYMBOLS}")
print(f"Timeframes: {[t.value for t in TIMEFRAMES]}")
print(f"Period: {START_DATE} to {END_DATE}")

# Monkey-patch the global variables in the module

module.SYMBOLS = SYMBOLS
module.TIMEFRAMES = TIMEFRAMES
module.START_DATE = START_DATE
module.END_DATE = END_DATE

# Now run
run_tick_backfill()
