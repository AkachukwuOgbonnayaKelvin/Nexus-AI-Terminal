import csv
import sqlite3

DB = "nexus_data.db"
TABLES = {
    "fact_tick": {
        "columns": [
            "symbol",
            "timestamp",
            "bid",
            "ask",
            "last",
            "volume",
            "source_id",
            "quality_score",
        ],
        "order": "timestamp",
    },
    "fact_ohlcv": {
        "columns": [
            "time",
            "symbol",
            "timeframe",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "source",
            "quality_score",
            "ingested_at",
        ],
        "order": "time",
    },
    "fact_volume": {
        "columns": [
            "symbol",
            "timeframe",
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "real_volume",
            "source_id",
            "quality_score",
        ],
        "order": "timestamp",
    },
    "fact_tick_aggregated": {
        "columns": [
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
            "zero_ticks",
            "pressure",
            "imbalance",
            "avg_spread",
            "max_spread",
            "min_spread",
            "source_id",
            "quality_score",
            "created_at",
        ],
        "order": "timestamp",
    },
}

conn = sqlite3.connect(DB)
for table, config in TABLES.items():
    cols = config["columns"]
    query = f"SELECT {', '.join(cols)} FROM {table} ORDER BY {config['order']}"
    print(f"Exporting {table}...")
    cur = conn.cursor()
    cur.execute(query)
    with open(f"{table}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)  # header
        writer.writerows(cur)
    print(f"Exported {table}.csv")
conn.close()
