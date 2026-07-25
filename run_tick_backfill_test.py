import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

# Patch the persistence before importing the backfill
from intelligence.data.tick import persistence
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter

persistence.TickWarehouseWriter = TickSQLiteWriter

# Import the original backfill after patching
import intelligence.data.tick.tests.run_tick_backfill as module
from intelligence.data.tick.contracts import Timeframe

# Override symbols and timeframes for a tiny test
module.SYMBOLS = ["EURUSD"]
module.TIMEFRAMES = [Timeframe.MINUTE_15]  # Only 15-minute aggregated data
module.START_DATE = datetime.utcnow() - timedelta(days=1)  # 1 day only
module.END_DATE = datetime.utcnow()

# Run the backfill
module.run_tick_backfill()
