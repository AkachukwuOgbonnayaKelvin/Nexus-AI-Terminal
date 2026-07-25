"""
Migrate legacy OHLCV pickle files into the warehouse.
Handles the missing class 'OHLCVData' by using a generic container.
"""

import os
import pickle
import sqlite3
from typing import Any

import pandas as pd

# ---- Compatibility layer ----


class DummyOHLCVData:
    """
    A generic class that mimics the original OHLCVData.
    It can accept any arguments and store them as attributes.
    """

    def __init__(self, *args, **kwargs):
        # The pickle may call __init__ with positional args or kwargs.
        # We store everything so we can extract later.
        self._args = args
        self._kwargs = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"DummyOHLCVData({self._kwargs})"


class CompatUnpickler(pickle.Unpickler):
    """Unpickler that maps missing classes to DummyOHLCVData."""

    def find_class(self, module, name):
        # If the class name contains 'OHLCVData' or is in a known legacy path,
        # map to our dummy.
        if "OHLCVData" in name or "OHLCV" in name or "Candle" in name:
            return DummyOHLCVData
        # Also map any missing class from providers.base
        if module.startswith("providers.") or module == "providers.base":
            return DummyOHLCVData
        # For anything else, fallback to DummyOHLCVData to avoid crashes
        return DummyOHLCVData


# ---- OHLCV extraction ----


def extract_ohlcv_from_object(obj: Any) -> pd.DataFrame | None:
    """
    Recursively extract OHLCV data from a legacy object.
    Returns a DataFrame with columns: time, open, high, low, close, volume.
    """
    if obj is None:
        return None

    # If it's a list, inspect the first element to determine structure
    if isinstance(obj, list):
        if len(obj) == 0:
            return None
        # Try to extract from each element
        records = []
        for item in obj:
            rec = extract_record(item)
            if rec:
                records.append(rec)
        if records:
            df = pd.DataFrame(records)
            # Ensure required columns exist
            required = ["time", "open", "high", "low", "close"]
            missing = [c for c in required if c not in df.columns]
            if missing:
                print(f"Missing columns: {missing}. Available: {df.columns.tolist()}")
                return None
            # Add volume if missing
            if "volume" not in df.columns:
                df["volume"] = 0
            return df
        else:
            return None

    # If it's a single object with attributes, try to extract
    if hasattr(obj, "__dict__"):
        rec = extract_record(obj)
        if rec:
            df = pd.DataFrame([rec])
            return df

    # If it's a dict, try to find lists inside
    if isinstance(obj, dict):
        # Look for keys like 'data', 'candles', 'bars', etc.
        for key in ["data", "candles", "bars", "ohlcv", "values"]:
            if key in obj and isinstance(obj[key], list):
                df = extract_ohlcv_from_object(obj[key])
                if df is not None:
                    return df
        # If we have time and price arrays directly
        if "time" in obj and "open" in obj:
            # Might be dict of arrays
            try:
                df = pd.DataFrame(obj)
                required = ["time", "open", "high", "low", "close"]
                if all(c in df.columns for c in required):
                    return df
            except Exception:
                pass
        return None

    return None


def extract_record(item: Any) -> dict | None:
    """
    Extract a single OHLCV record from a legacy object.
    """
    if item is None:
        return None

    # If it's a dict, try to get fields directly
    if isinstance(item, dict):
        required = ["time", "open", "high", "low", "close"]
        if all(k in item for k in required):
            rec = {k: item[k] for k in required}
            rec["volume"] = item.get("volume", 0)
            return rec
        # Try with alternative names
        alt = {
            "timestamp": "time",
            "date": "time",
            "datetime": "time",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume",
        }
        rec = {}
        for k, v in item.items():
            if k in alt:
                rec[alt[k]] = v
            else:
                rec[k] = v
        if (
            "time" in rec
            and "open" in rec
            and "high" in rec
            and "low" in rec
            and "close" in rec
        ):
            rec["volume"] = rec.get("volume", 0)
            return rec
        return None

    # If it's an object with attributes
    if hasattr(item, "__dict__"):
        _d = item.__dict__
        # Try common attribute names
        rec = {}
        for attr in [
            "time",
            "timestamp",
            "date",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]:
            if hasattr(item, attr):
                rec[attr] = getattr(item, attr)
        # Normalize time field
        if "time" not in rec and "timestamp" in rec:
            rec["time"] = rec.pop("timestamp")
        if "time" in rec:
            # Check if required fields exist
            required = ["time", "open", "high", "low", "close"]
            if all(k in rec for k in required):
                rec["volume"] = rec.get("volume", 0)
                return rec
        # Also try to use _kwargs
        if hasattr(item, "_kwargs") and isinstance(item._kwargs, dict):
            return extract_record(item._kwargs)
        # Try to use _args (may contain a tuple of values)
        if hasattr(item, "_args") and item._args:
            # Could be (timestamp, open, high, low, close, volume)
            if len(item._args) >= 5:
                args = item._args
                rec = {
                    "time": args[0],
                    "open": args[1],
                    "high": args[2],
                    "low": args[3],
                    "close": args[4],
                }
                if len(args) > 5:
                    rec["volume"] = args[5]
                else:
                    rec["volume"] = 0
                return rec
        return None

    return None


# ---- Database import ----


def import_df_to_db(
    df: pd.DataFrame, symbol: str, timeframe: str, db_path: str = "nexus_data.db"
):
    """
    Import a DataFrame of OHLCV data into the warehouse.
    Adds symbol, timeframe, source columns.
    """
    # Ensure time is datetime
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])
    # Add metadata
    df["symbol"] = symbol
    df["timeframe"] = timeframe
    df["source"] = "legacy_pickle"
    # Ensure columns order
    cols = [
        "time",
        "symbol",
        "timeframe",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "source",
    ]
    df = df[cols]

    conn = sqlite3.connect(db_path)
    # Create table if not exists (with proper schema)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TIMESTAMP NOT NULL,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            source TEXT
        )
    """)
    # Create indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_price_time ON prices(time)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_price_symbol ON prices(symbol)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_price_timeframe ON prices(timeframe)")
    conn.commit()
    # Insert data
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()
    return len(df)


# ---- Main migration ----


def parse_filename(filename: str):
    """Parse symbol and timeframe from filename like 'EURUSD_D1.pkl'."""
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

    success = []
    failed = []

    for fname in files:
        symbol, timeframe = parse_filename(fname)
        filepath = os.path.join(data_dir, fname)
        print(f"Processing {fname} ...", end=" ")
        try:
            with open(filepath, "rb") as f:
                unpickler = CompatUnpickler(f)
                obj = unpickler.load()
            df = extract_ohlcv_from_object(obj)
            if df is None or df.empty:
                print("❌ No OHLCV data found")
                failed.append((fname, "No data extracted"))
                continue
            # Clean and import
            # Remove any rows with NaN
            df = df.dropna(subset=["open", "high", "low", "close"])
            if df.empty:
                print("❌ All rows had NaN")
                failed.append((fname, "All NaN"))
                continue
            # Convert time to datetime
            df["time"] = pd.to_datetime(df["time"])
            # Import
            rows = import_df_to_db(df, symbol, timeframe, db_path)
            print(f"✅ Imported {rows} rows")
            success.append((fname, rows))
        except Exception as e:
            print(f"❌ Error: {e}")
            failed.append((fname, str(e)))

    print("\n=== Migration Summary ===")
    print(f"Success: {len(success)} files")
    for fname, rows in success:
        print(f"  {fname}: {rows} rows")
    print(f"Failed: {len(failed)} files")
    for fname, err in failed:
        print(f"  {fname}: {err}")


if __name__ == "__main__":
    migrate_all()
