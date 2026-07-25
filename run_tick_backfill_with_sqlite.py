import os
import sys

sys.path.insert(0, os.getcwd())

# Import the original backfill module
import intelligence.data.tick.tests.run_tick_backfill as original
from intelligence.data.tick import persistence

# Override the persistence module's TickWarehouseWriter
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter

persistence.TickWarehouseWriter = TickSQLiteWriter

# Also override NDIPTickWriter if needed (we can use our SQLite for NDIP too, but for now we just need warehouse)

# Now run the original backfill
original.run_tick_backfill()
