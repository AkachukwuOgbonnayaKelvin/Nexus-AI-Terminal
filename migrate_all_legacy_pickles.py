import os
import pickle
import sqlite3
import struct
from datetime import datetime

# ---- Compatibility layer ----


class DummyOHLCVData:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)


class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if "OHLCVData" in name or "OHLCV" in name or "Candle" in name:
            return DummyOHLCVData
        if module.startswith("providers.") or module == "providers.base":
            return DummyOHLCVData
        if module == "__main__.base" and name == "OHLCVData":
            return DummyOHLCVData
        return DummyOHLCVData


# ---- Timestamp decoder ----


def decode_timestamp_bytes(data: bytes) -> datetime:
    """
    Decode legacy timestamp format:
    year (2 bytes, big-endian)
    month (1 byte)
    day (1 byte)
    hour (1 byte)
    minute (1 byte)
    second (1 byte)
    microsecond (4 bytes, big-endian) – but likely zeros
    """
    if len(data) < 8:
        raise ValueError(f"Timestamp bytes too short: {data!r}")
    # Unpack assuming big-endian
    year = struct.unpack(">H", data[0:2])[0]
    month = data[2]
    day = data[3]
    hour = data[4]
    minute = data[5] if len(data) > 5 else 0
    second = data[6] if len(data) > 6 else 0
    micro = data[7] if len(data) > 7 else 0
    # If there are more bytes, they might be microsecond (4 bytes)
    if len(data) >= 11:
        micro = struct.unpack(">I", data[7:11])[0]
    return datetime(year, month, day, hour, minute, second, micro)


# ---- Extract records ----


def extract_candle(obj: DummyOHLCVData) -> dict:
    """Convert a single DummyOHLCVData to a dict with decoded timestamp."""
    # timestamp attribute is bytes
    ts_bytes = getattr(obj, "timestamp", None)
    if ts_bytes is None:
        raise ValueError("Missing timestamp")
    if isinstance(ts_bytes, bytes):
        timestamp = decode_timestamp_bytes(ts_bytes)
    else:
        # fallback: if it's already a datetime, use it
        if isinstance(ts_bytes, datetime):
            timestamp = ts_bytes
        else:
            raise ValueError(f"Unexpected timestamp type: {type(ts_bytes)}")
    return {
        "symbol": getattr(obj, "symbol", ""),
        "timeframe": getattr(obj, "timeframe", ""),
        "timestamp": timestamp,
        "open": float(getattr(obj, "open", 0.0)),
        "high": float(getattr(obj, "high", 0.0)),
        "low": float(getattr(obj, "low", 0.0)),
        "close": float(getattr(obj, "close", 0.0)),
        "volume": float(getattr(obj, "volume", 0.0)),
        "source": getattr(obj, "source", "legacy_pickle"),
        "quality_score": float(getattr(obj, "quality_score", 0.0)),
    }


def extract_all_from_pickle(filepath: str) -> list[dict]:
    with open(filepath, "rb") as f:
        unpickler = CompatUnpickler(f)
        obj = unpickler.load()
    if not isinstance(obj, list):
        raise ValueError(f"Expected list, got {type(obj)}")
    records = []
    for item in obj:
        if isinstance(item, DummyOHLCVData):
            rec = extract_candle(item)
            # Validate OHLC
            if rec["high"] < rec["low"]:
                raise ValueError(f"High < Low: {rec}")
            if rec["high"] < rec["open"] or rec["high"] < rec["close"]:
                raise ValueError(f"High invalid: {rec}")
            if rec["low"] > rec["open"] or rec["low"] > rec["close"]:
                raise ValueError(f"Low invalid: {rec}")
            records.append(rec)
        else:
            # Skip non-candle objects
            continue
    return records


# ---- Database persistence ----


def insert_records_to_db(records: list[dict], db_path: str = "nexus_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP NOT NULL,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            source TEXT,
            quality_score REAL,
            UNIQUE(symbol, timeframe, timestamp)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_time ON prices(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_symbol ON prices(symbol)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_price_timeframe ON prices(timeframe)"
    )
    conn.commit()

    inserted = 0
    for rec in records:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO prices
                (timestamp, symbol, timeframe, open, high, low, close, volume, source, quality_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    rec["timestamp"],
                    rec["symbol"],
                    rec["timeframe"],
                    rec["open"],
                    rec["high"],
                    rec["low"],
                    rec["close"],
                    rec["volume"],
                    rec["source"],
                    rec["quality_score"],
                ),
            )
            if cursor.rowcount > 0:
                inserted += 1
        except Exception as e:
            print(f"Error inserting {rec}: {e}")
    conn.commit()
    conn.close()
    return inserted


# ---- Main migration runner ----


def parse_filename(filename: str):
    name = filename.replace(".pkl", "")
    if "_" in name:
        parts = name.rsplit("_", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
    return name, "unknown"


def migrate_all(
    data_dir: str = "market_price_engine/data", db_path: str = "nexus_data.db"
):
    files = [
        f for f in os.listdir(data_dir) if f.endswith(".pkl") and f != "load_state.json"
    ]
    print(f"Found {len(files)} pickle files.")
    total_inserted = 0
    success = []
    failed = []

    for fname in files:
        filepath = os.path.join(data_dir, fname)
        print(f"Processing {fname} ...", end=" ")
        try:
            records = extract_all_from_pickle(filepath)
            if not records:
                print("❌ No records extracted")
                failed.append((fname, "No records"))
                continue
            # Override symbol and timeframe from filename (in case object doesn't have them)
            symbol, timeframe = parse_filename(fname)
            for rec in records:
                if not rec["symbol"]:
                    rec["symbol"] = symbol
                if not rec["timeframe"]:
                    rec["timeframe"] = timeframe
            inserted = insert_records_to_db(records, db_path)
            total_inserted += inserted
            print(f"✅ Inserted {inserted} rows")
            success.append((fname, inserted))
        except Exception as e:
            print(f"❌ Error: {e}")
            failed.append((fname, str(e)))

    print("\n=== Migration Summary ===")
    print(f"Success: {len(success)} files")
    for fname, rows in success:
        print(f"  {fname}: {rows} rows")
    print(f"Failed: {len(failed)} files")
    for fname, err in failed[:10]:
        print(f"  {fname}: {err}")
    print(f"Total inserted: {total_inserted}")


if __name__ == "__main__":
    migrate_all()
