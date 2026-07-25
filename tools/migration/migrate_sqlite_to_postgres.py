import os
import sqlite3

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

SQLITE_DB = "nexus_data.db"
PGPASSWORD = os.getenv("PGPASSWORD", "")
POSTGRES_DSN = (
    f"dbname=nexus_ai_terminal user=postgres password={PGPASSWORD} host=localhost"
)

TABLES = {
    "fact_tick": {
        "target": "raw.market_ticks",
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
        "target_columns": [
            "symbol",
            "time",
            "bid",
            "ask",
            "last",
            "volume",
            "source_id",
            "quality_score",
        ],
        "time_col": "timestamp",
    },
    "fact_ohlcv": {
        "target": "raw.market_ohlcv",
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
        "target_columns": [
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
        "time_col": "time",
    },
    "fact_volume": {
        "target": "raw.market_volume",
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
        "target_columns": [
            "symbol",
            "timeframe",
            "time",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "real_volume",
            "source_id",
            "quality_score",
        ],
        "time_col": "timestamp",
    },
    "fact_tick_aggregated": {
        "target": "raw.tick_aggregates",
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
        "target_columns": [
            "symbol",
            "timeframe",
            "time",
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
        "time_col": "timestamp",
    },
}


def migrate_table(sqlite_conn, pg_conn, table_name, config, chunk_size=100000):
    print(f"Migrating {table_name}...")
    cursor = sqlite_conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total = cursor.fetchone()[0]
    print(f"Total rows: {total:,}")

    if total == 0:
        print("Skipping empty table.")
        return

    offset = 0
    inserted = 0
    while offset < total:
        cols = config["columns"]
        query = f"SELECT {', '.join(cols)} FROM {table_name} ORDER BY {config['time_col']} LIMIT {chunk_size} OFFSET {offset}"
        df = pd.read_sql_query(query, sqlite_conn)

        if df.empty:
            break

        if config["time_col"] == "timestamp":
            df.rename(columns={"timestamp": "time"}, inplace=True)

        target_cols = config["target_columns"]
        for col in target_cols:
            if col not in df.columns:
                df[col] = None

        df = df[target_cols]
        records = list(df.to_records(index=False))

        insert_sql = (
            f"INSERT INTO {config['target']} ({', '.join(target_cols)}) VALUES %s"
        )
        pg_cursor = pg_conn.cursor()
        try:
            execute_values(pg_cursor, insert_sql, records, page_size=chunk_size)
            pg_conn.commit()
            inserted += len(records)
            print(f"Inserted {inserted:,} rows")
        except Exception as e:
            print(f"Error: {e}")
            pg_conn.rollback()
            break

        offset += chunk_size

    print(f"Finished migrating {table_name}. Total inserted: {inserted:,}")


def main():
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    pg_conn = psycopg2.connect(POSTGRES_DSN)

    for table_name, config in TABLES.items():
        migrate_table(sqlite_conn, pg_conn, table_name, config)

    sqlite_conn.close()
    pg_conn.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
