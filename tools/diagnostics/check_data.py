import os
import sqlite3


def check_db(db_path, label):
    print(f"\n=== {label} ===")
    if not os.path.exists(db_path):
        print(f"  Database file not found: {db_path}")
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    if not tables:
        print("  No tables found.")
    else:
        for (tbl,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
            count = cursor.fetchone()[0]
            print(f"  {tbl}: {count}")
    conn.close()


check_db("nexus_data.db", "Main Data (OHLC, Tick, Volume)")
check_db("nexus_sentiment.db", "Sentiment Engine")
