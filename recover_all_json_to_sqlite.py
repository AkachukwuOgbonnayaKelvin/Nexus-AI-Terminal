import json
import os
import sqlite3

DB_PATH = "nexus_data.db"


def create_tables(conn):
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ndip_raw_tick (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT, timestamp TEXT,
            bid REAL, ask REAL, last REAL, volume REAL,
            source_id TEXT, retrieved_at TEXT,
            UNIQUE(symbol, timestamp, source_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS ndip_classified_tick (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT, timestamp TEXT,
            bid REAL, ask REAL, last REAL, volume REAL,
            direction TEXT, pressure REAL,
            source_id TEXT,
            UNIQUE(symbol, timestamp, source_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS ndip_aggregated_tick (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT, timeframe TEXT, timestamp TEXT,
            open REAL, high REAL, low REAL, close REAL,
            tick_count INTEGER, up_ticks INTEGER, down_ticks INTEGER,
            pressure REAL, imbalance REAL,
            source_id TEXT,
            UNIQUE(symbol, timeframe, timestamp, source_id)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS ndip_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT, timestamp TEXT,
            quality_score REAL, details TEXT,
            UNIQUE(symbol, timestamp)
        )
    """)
    conn.commit()


def process_json_file(filepath, table, mapping):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return 0

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    decoder = json.JSONDecoder()
    buffer = ""
    count = 0

    with open(filepath, "r", encoding="utf-8") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            buffer += chunk
            while buffer:
                try:
                    obj, idx = decoder.raw_decode(buffer)
                    buffer = buffer[idx:].lstrip()
                    # Map object fields to table columns
                    values = [obj.get(k, None) for k in mapping]
                    placeholders = ",".join(["?"] * len(mapping))
                    c.execute(
                        f"INSERT OR IGNORE INTO {table} ({','.join(mapping)}) VALUES ({placeholders})",
                        values,
                    )
                    count += 1
                    if count % 10000 == 0:
                        conn.commit()
                        print(f"  Inserted {count} records")
                except json.JSONDecodeError:
                    break
    conn.commit()
    conn.close()
    print(f"  Total inserted into {table}: {count}")
    return count


def main():
    print("=== RECOVER TICK JSON TO SQLITE ===")

    # Define file mappings
    files = [
        (
            "./data/ndip/tick/raw.json",
            "ndip_raw_tick",
            ["symbol", "timestamp", "bid", "ask", "last", "volume", "source_id"],
        ),
        (
            "./data/ndip/tick/classified.json",
            "ndip_classified_tick",
            [
                "symbol",
                "timestamp",
                "bid",
                "ask",
                "last",
                "volume",
                "direction",
                "pressure",
                "source_id",
            ],
        ),
        (
            "./data/ndip/tick/aggregated.json",
            "ndip_aggregated_tick",
            [
                "symbol",
                "timeframe",
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "tick_count",
                "up_ticks",
                "down_ticks",
                "pressure",
                "imbalance",
                "source_id",
            ],
        ),
        (
            "./data/ndip/tick/quality.json",
            "ndip_quality",
            ["symbol", "timestamp", "quality_score", "details"],
        ),
    ]

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    conn.close()

    total = 0
    for filepath, table, mapping in files:
        print(f"\nProcessing {filepath}")
        count = process_json_file(filepath, table, mapping)
        total += count

    print(f"\n✅ Total records recovered: {total}")


if __name__ == "__main__":
    main()
