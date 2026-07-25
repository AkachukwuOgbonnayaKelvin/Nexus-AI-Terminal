import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

# Import original backfill components
from intelligence.data.tick.backfill import TickBackfillConfig, TickBackfillScheduler
from intelligence.data.tick.contracts import Timeframe
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter


# Create our NDIP SQLite writer (will be patched)
class NDIPSQLiteWriter:
    def __init__(self, db_path: str = "nexus_data.db"):
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self):
        import sqlite3

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS ndip_raw_tick (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                bid REAL, ask REAL, last REAL, volume REAL,
                source_id TEXT,
                retrieved_at TEXT,
                UNIQUE(symbol, timestamp, source_id)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS ndip_classified_tick (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                bid REAL, ask REAL, last REAL, volume REAL,
                direction TEXT, pressure REAL,
                source_id TEXT,
                UNIQUE(symbol, timestamp, source_id)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS ndip_aggregated_tick (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                open REAL, high REAL, low REAL, close REAL,
                tick_count INTEGER,
                up_ticks INTEGER, down_ticks INTEGER,
                pressure REAL, imbalance REAL,
                source_id TEXT,
                UNIQUE(symbol, timeframe, timestamp, source_id)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS ndip_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                quality_score REAL,
                details TEXT,
                UNIQUE(symbol, timestamp)
            )
        """)
        conn.commit()
        conn.close()

    def write_raw(self, ticks):
        # Convert tick objects to dicts and insert
        import sqlite3

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        now = datetime.utcnow().isoformat()
        count = 0
        for t in ticks:
            try:
                c.execute(
                    """
                    INSERT OR IGNORE INTO ndip_raw_tick
                    (symbol, timestamp, bid, ask, last, volume, source_id, retrieved_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        t.symbol,
                        t.timestamp.isoformat(),
                        t.bid,
                        t.ask,
                        t.last,
                        t.volume,
                        t.source_id,
                        now,
                    ),
                )
                count += c.rowcount
            except Exception as e:
                print(f"NDIP raw insert error: {e}")
        conn.commit()
        conn.close()
        return count

    # Other methods will be added as needed, but we can stub them to avoid errors
    def write_classified(self, ticks):
        return 0

    def write_aggregated(self, agg):
        return 0

    def write_quality(self, symbol, timestamp, quality):
        return 0

    def write_provenance(self, records):
        return 0


# Patch the persistence module
from intelligence.data.tick import persistence

persistence.NDIPTickWriter = NDIPSQLiteWriter
persistence.TickWarehouseWriter = TickSQLiteWriter

# Override backfill parameters
SYMBOLS = ["EURUSD"]
TIMEFRAMES = [Timeframe.MINUTE_15]
END_DATE = datetime.utcnow()
START_DATE = END_DATE - timedelta(days=1)  # 1 day test

config = TickBackfillConfig(
    symbols=SYMBOLS,
    timeframes=TIMEFRAMES,
    start_date=START_DATE,
    end_date=END_DATE,
    batch_size_hours=1,
    max_ticks_per_batch=20000,
    max_retries=2,
    retry_delay_seconds=30,
    min_quality_score=0.5,
    checkpoint_file="./data/tick_backfill_patched_checkpoint.json",
)

scheduler = TickBackfillScheduler(config, parallel_workers=1)
scheduler.run()
