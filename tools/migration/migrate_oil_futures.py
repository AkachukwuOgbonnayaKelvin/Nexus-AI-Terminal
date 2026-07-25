import os
import pickle
import sqlite3
import struct
from datetime import datetime
from typing import Any

# ---- Compatibility ----


class CompatObject:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                setattr(self, k, v)

    # In case the unpickler tries to call this object as a function
    def __call__(self, *args, **kwargs):
        # Return a list of candles (dummy) to avoid errors
        return []


class CompatUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        return CompatObject


# ---- Timestamp extraction ----


def extract_raw_value(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (int, float, str, bool, datetime, bytes)):
        return obj
    if isinstance(obj, CompatObject):
        # Check _args first
        if hasattr(obj, "_args") and obj._args:
            return extract_raw_value(obj._args[0])
        if hasattr(obj, "_kwargs"):
            for key in ["timestamp", "time", "date", "datetime"]:
                if key in obj._kwargs:
                    return extract_raw_value(obj._kwargs[key])
        for attr in ["timestamp", "time", "date", "datetime"]:
            if hasattr(obj, attr):
                return extract_raw_value(getattr(obj, attr))
        return None
    if isinstance(obj, list):
        if obj:
            return extract_raw_value(obj[0])
        return None
    if isinstance(obj, dict):
        for key in ["timestamp", "time", "date", "datetime"]:
            if key in obj:
                return extract_raw_value(obj[key])
        return None
    return obj


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
    raw = extract_raw_value(obj)
    if raw is None:
        raise ValueError("Timestamp not found")
    if isinstance(raw, datetime):
        return raw
    if isinstance(raw, bytes):
        return decode_timestamp_bytes(raw)
    if isinstance(raw, (int, float)):
        return datetime.fromtimestamp(raw)
    raise ValueError(f"Unexpected timestamp type: {type(raw)}")


# ---- Extract candle ----


def get_field(obj, name):
    if hasattr(obj, name):
        return getattr(obj, name)
    if hasattr(obj, "_kwargs") and name in obj._kwargs:
        return obj._kwargs[name]
    if hasattr(obj, "_args"):
        args = obj._args
        if name == "timestamp" and len(args) > 0:
            return args[0]
        if name == "open" and len(args) > 1:
            return args[1]
        if name == "high" and len(args) > 2:
            return args[2]
        if name == "low" and len(args) > 3:
            return args[3]
        if name == "close" and len(args) > 4:
            return args[4]
        if name == "volume" and len(args) > 5:
            return args[5]
    return None


def extract_candle(obj: Any) -> dict:
    ts_raw = get_field(obj, "timestamp")
    if ts_raw is None:
        raise ValueError("Timestamp not found")
    timestamp = extract_timestamp(ts_raw)

    open_val = float(get_field(obj, "open") or 0.0)
    high_val = float(get_field(obj, "high") or 0.0)
    low_val = float(get_field(obj, "low") or 0.0)
    close_val = float(get_field(obj, "close") or 0.0)
    volume_val = float(get_field(obj, "volume") or 0.0)
    symbol = get_field(obj, "symbol") or ""
    timeframe = get_field(obj, "timeframe") or ""
    source = get_field(obj, "source") or "legacy_pickle"
    quality = float(get_field(obj, "quality_score") or 0.0)

    if high_val < low_val:
        raise ValueError(f"High < Low: {high_val} < {low_val}")
    if high_val < open_val or high_val < close_val:
        raise ValueError(f"High invalid: {high_val}")
    if low_val > open_val or low_val > close_val:
        raise ValueError(f"Low invalid: {low_val}")

    return {
        "time": timestamp,
        "symbol": symbol,
        "timeframe": timeframe,
        "open": open_val,
        "high": high_val,
        "low": low_val,
        "close": close_val,
        "volume": volume_val,
        "source": source,
        "quality_score": quality,
    }


def extract_from_pickle(filepath: str) -> list[dict]:
    with open(filepath, "rb") as f:
        unpickler = CompatUnpickler(f)
        obj = unpickler.load()
    if not isinstance(obj, list):
        raise ValueError(f"Expected list, got {type(obj)}")
    records = []
    for item in obj:
        if hasattr(item, "timestamp") or hasattr(item, "_args"):
            try:
                rec = extract_candle(item)
                records.append(rec)
            except Exception as e:
                print(f"  Skipping item due to error: {e}")
        else:
            continue
    return records


def insert_records(records: list[dict], db_path: str = "nexus_data.db") -> int:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
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


def main():
    data_dir = "market_price_engine/data"
    files = [
        "BZ=F_D1.pkl",
        "BZ=F_H1.pkl",
        "BZ=F_H4.pkl",
        "CL=F_D1.pkl",
        "CL=F_H1.pkl",
        "CL=F_H4.pkl",
    ]
    total = 0
    for fname in files:
        filepath = os.path.join(data_dir, fname)
        if not os.path.exists(filepath):
            print(f"File not found: {fname}")
            continue
        print(f"Processing {fname} ...", end=" ")
        try:
            records = extract_from_pickle(filepath)
            if not records:
                print("❌ No records extracted")
                continue
            # Override symbol and timeframe from filename (if not present)
            symbol = fname.split("_")[0]
            timeframe = fname.split("_")[1].replace(".pkl", "")
            for rec in records:
                if not rec["symbol"]:
                    rec["symbol"] = symbol
                if not rec["timeframe"]:
                    rec["timeframe"] = timeframe
            inserted = insert_records(records)
            total += inserted
            print(f"✅ Inserted {inserted} rows")
        except Exception as e:
            print(f"❌ Error: {e}")
    print(f"\nTotal inserted from oil futures: {total}")


if __name__ == "__main__":
    main()
