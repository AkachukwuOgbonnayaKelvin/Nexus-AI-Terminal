import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

# Patch BOTH writers BEFORE importing the backfill
from intelligence.data.tick import persistence
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter

# Replace both NDIP and Warehouse writers with SQLite versions
persistence.NDIPTickWriter = TickSQLiteWriter
persistence.TickWarehouseWriter = TickSQLiteWriter

# Now import the original backfill (after patching)
import intelligence.data.tick.tests.run_tick_backfill as module
from intelligence.data.tick.contracts import Timeframe

# Override with a tiny test (1 symbol, 1 timeframe, 1 day)
module.SYMBOLS = ["EURUSD"]
module.TIMEFRAMES = [Timeframe.MINUTE_15]
module.START_DATE = datetime.utcnow() - timedelta(days=1)
module.END_DATE = datetime.utcnow()

# Run
module.run_tick_backfill()
