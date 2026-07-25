import os
import pickle
import sqlite3
import struct
from datetime import datetime
from typing import Any

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
    if len(data) < 8:
        raise ValueError(f"Timestamp bytes too short: {data!r}")
    year = struct.unpack(">H", data[0:2])[0]
    month = data[2]
    day = data[3]
    hour = data[4]
    minute = data[5] if len(data) > 5 else 0
    second = data[6] if len(data) > 6 else 0
    micro = 0
    if len(data) >= 11:
        micro = struct.unpack(">I", data[7:11])[0]
    return datetime(year, month, day, hour, minute, second, micro)


def extract_timestamp(obj: Any) -> datetime:
    if obj is None:
        raise ValueError("Timestamp is None")
    if isinstance(obj, datetime):
        return obj
    if isinstance(obj, bytes):
        return decode_timestamp_bytes(obj)
    if hasattr(obj, "__class__") and obj.__class__.__name__ == "DummyOHLCVData":
        if hasattr(obj, "_args") and obj._args:
            return extract_timestamp(obj._args[0])
        if hasattr(obj, "_kwargs"):
            for key in ["timestamp", "time", "date", "datetime"]:
                if key in obj._kwargs:
                    return extract_timestamp(obj._kwargs[key])
        for attr in ["timestamp", "time", "date", "datetime"]:
            if hasattr(obj, attr):
                return extract_timestamp(getattr(obj, attr))
    if isinstance(obj, dict):
        for key in ["timestamp", "time", "date", "datetime"]:
            if key in obj:
                return extract_timestamp(obj[key])
    if hasattr(obj, "__dict__"):
        for attr in ["timestamp", "time", "date", "datetime"]:
            if hasattr(obj, attr):
                return extract_timestamp(getattr(obj, attr))
    if isinstance(obj, (int, float)):
        try:
            return datetime.fromtimestamp(obj)
        except Exception:
            raise ValueError(f"Cannot convert number to datetime: {obj}")
    raise ValueError(f"Unexpected timestamp type: {type(obj)}")


# ---- Extract records ----


def extract_candle(obj: Any) -> dict:
    if not hasattr(obj, "timestamp"):
        raise ValueError("Object has no 'timestamp' attribute")
    timestamp = extract_timestamp(obj.timestamp)
    open_val = float(getattr(obj, "open", 0.0))
    high_val = float(getattr(obj, "high", 0.0))
    low_val = float(getattr(obj, "low", 0.0))
    close_val = float(getattr(obj, "close", 0.0))
    volume_val = float(getattr(obj, "volume", 0.0))

    if high_val < low_val:
        raise ValueError(f"High < Low: {high_val} < {low_val}")
    if high_val < open_val or high_val < close_val:
        raise ValueError(f"High invalid: {high_val}")
    if low_val > open_val or low_val > close_val:
        raise ValueError(f"Low invalid: {low_val}")

    return {
        "time": timestamp,
        "symbol": getattr(obj, "symbol", ""),
        "timeframe": getattr(obj, "timeframe", ""),
        "open": open_val,
        "high": high_val,
        "low": low_val,
        "close": close_val,
        "volume": volume_val,
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
        if hasattr(item, "timestamp"):
            try:
                rec = extract_candle(item)
                records.append(rec)
            except Exception as e:
                print(f"  Skipping candle due to error: {e}")
        else:
            continue
    return records


# ---- Database persistence ----


def insert_records_to_db(records: list[dict], db_path: str = "nexus_data.db") -> int:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop old table if exists (optional; comment out to keep existing data)
    # cursor.execute('DROP TABLE IF EXISTS prices')
    # cursor.execute('DROP TABLE IF EXISTS fact_ohlcv')

    # Create canonical table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_ohlcv (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TIMESTAMP NOT NULL,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL,
            source TEXT,
            quality_score REAL,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, timeframe, time)
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ohlcv_time ON fact_ohlcv(time)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ohlcv_symbol ON fact_ohlcv(symbol)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_ohlcv_timeframe ON fact_ohlcv(timeframe)"
    )
    conn.commit()

    inserted = 0
    for rec in records:
        try:
            cursor.execute(
                """
                INSERT OR IGNORE INTO fact_ohlcv
                (time, symbol, timeframe, open, high, low, close, volume, source, quality_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    rec["time"],
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
