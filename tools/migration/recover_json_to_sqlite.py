import json
import sqlite3
from datetime import datetime

JSON_PATH = "./data/ndip/tick/raw.json"  # adjust to your actual path
DB_PATH = "nexus_data.db"


def recover_json_in_chunks(filepath, chunk_size=10000):
    conn = sqlite3.connect(DB_PATH)
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
    conn.commit()

    with open(filepath, "r", encoding="utf-8") as f:
        decoder = json.JSONDecoder()
        buffer = ""
        count = 0
        while True:
            chunk = f.read(1024 * 1024)  # 1 MB chunks
            if not chunk:
                break
            buffer += chunk
            while buffer:
                try:
                    obj, idx = decoder.raw_decode(buffer)
                    buffer = buffer[idx:].lstrip()
                    c.execute(
                        """
                        INSERT OR IGNORE INTO ndip_raw_tick
                        (symbol, timestamp, bid, ask, last, volume, source_id, retrieved_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            obj.get("symbol"),
                            obj.get("timestamp"),
                            obj.get("bid"),
                            obj.get("ask"),
                            obj.get("last"),
                            obj.get("volume"),
                            obj.get("source_id"),
                            datetime.utcnow().isoformat(),
                        ),
                    )
                    count += 1
                    if count % chunk_size == 0:
                        conn.commit()
                        print(f"Inserted {count} records")
                except json.JSONDecodeError:
                    break
        conn.commit()
        print(f"Total inserted: {count}")
    conn.close()


def main():
    filepath = JSON_PATH
    recover_json_in_chunks(filepath, chunk_size=10000)


if __name__ == "__main__":
    main()
