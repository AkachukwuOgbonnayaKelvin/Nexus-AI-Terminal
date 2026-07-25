import os
import pickle
import sqlite3

import pandas as pd

DATA_DIR = "market_price_engine/data"
DB_PATH = "nexus_data.db"


def parse_filename(filename):
    """Extract symbol and timeframe from filename like 'EURUSD_D1.pkl'."""
    name = filename.replace(".pkl", "")
    # Split by '_' – assume last part is timeframe, rest is symbol
    parts = name.split("_")
    if len(parts) >= 2:
        timeframe = parts[-1]
        symbol = "_".join(parts[:-1])
        return symbol, timeframe
    else:
        return name, "unknown"


def standardise_df(df, symbol, timeframe):
    """Ensure DataFrame has columns: time, symbol, open, high, low, close, volume, source."""
    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"Expected DataFrame, got {type(df)}")
    # Ensure datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"])
            df.set_index("time", inplace=True)
        else:
            # try to convert first column to datetime
            df.index = pd.to_datetime(df.index)
    # Sort by date
    df = df.sort_index()
    # Standardise column names
    col_mapping = {}
    for col in df.columns:
        lower = col.lower()
        if lower in ["open", "o"]:
            col_mapping[col] = "open"
        elif lower in ["high", "h"]:
            col_mapping[col] = "high"
        elif lower in ["low", "l"]:
            col_mapping[col] = "low"
        elif lower in ["close", "c", "price"]:
            col_mapping[col] = "close"
        elif lower in ["volume", "vol"]:
            col_mapping[col] = "volume"
    if col_mapping:
        df = df.rename(columns=col_mapping)
    # Ensure required columns exist
    needed = ["open", "high", "low", "close"]
    for col in needed:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    # Add symbol, timeframe, source
    df["symbol"] = symbol
    df["timeframe"] = timeframe
    df["source"] = "pickle"
    # Add volume if missing
    if "volume" not in df.columns:
        df["volume"] = 0
    # Reset index to column
    df.reset_index(inplace=True)
    df.rename(columns={"index": "time"}, inplace=True)
    # Ensure time is datetime
    df["time"] = pd.to_datetime(df["time"])
    return df[
        [
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
    ]


def import_all():
    # List all pkl files
    files = [
        f for f in os.listdir(DATA_DIR) if f.endswith(".pkl") and f != "load_state.json"
    ]
    print(f"Found {len(files)} pickle files.")

    # Connect to database (create if not exists)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
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
    # Create index for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_time ON prices(time)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_symbol ON prices(symbol)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_price_timeframe ON prices(timeframe)"
    )
    conn.commit()

    total = 0
    for fname in files:
        symbol, timeframe = parse_filename(fname)
        filepath = os.path.join(DATA_DIR, fname)
        try:
            with open(filepath, "rb") as f:
                df_raw = pickle.load(f)
            df_std = standardise_df(df_raw, symbol, timeframe)
            # Insert into database
            df_std.to_sql("prices", conn, if_exists="append", index=False)
            total += len(df_std)
            print(f"Imported {fname} → {symbol} {timeframe} ({len(df_std)} rows)")
        except Exception as e:
            print(f"Error importing {fname}: {e}")

    conn.close()
    print(f"\n✅ Imported {total} total rows into {DB_PATH}")


if __name__ == "__main__":
    import_all()
