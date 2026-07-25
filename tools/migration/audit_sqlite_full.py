import json
import sqlite3

DB = "nexus_data.db"


def get_table_info(conn, table):
    cur = conn.cursor()
    info = {
        "table": table,
        "rows": 0,
        "columns": [],
        "time_column": None,
        "min_time": None,
        "max_time": None,
        "symbols": 0,
        "symbol_list": [],
        "timeframes": 0,
        "timeframe_list": [],
        "sample": [],
        "duplicates": 0,
        "duplicate_examples": [],
        "invalid_ohlc": 0,
        "null_counts": {},
        "database_size_mb": 0,
    }

    # Get column info
    cur.execute(f'PRAGMA table_info("{table}")')
    columns = cur.fetchall()
    info["columns"] = [col[1] for col in columns]

    # Total rows
    cur.execute(f'SELECT COUNT(*) FROM "{table}"')
    info["rows"] = cur.fetchone()[0]
    if info["rows"] == 0:
        return info

    # Detect time column (prefer 'timestamp', then 'time')
    time_col = None
    for col in info["columns"]:
        if col.lower() in ["timestamp", "time", "datetime", "date"]:
            time_col = col
            break
    info["time_column"] = time_col

    # Time range
    if time_col:
        try:
            cur.execute(f'SELECT MIN({time_col}), MAX({time_col}) FROM "{table}"')
            row = cur.fetchone()
            info["min_time"] = row[0]
            info["max_time"] = row[1]
        except Exception:
            pass

    # Distinct symbols
    if "symbol" in info["columns"]:
        cur.execute(f'SELECT COUNT(DISTINCT symbol) FROM "{table}"')
        info["symbols"] = cur.fetchone()[0]
        cur.execute(f'SELECT DISTINCT symbol FROM "{table}" ORDER BY symbol LIMIT 20')
        info["symbol_list"] = [row[0] for row in cur.fetchall()]

    # Distinct timeframes
    if "timeframe" in info["columns"]:
        cur.execute(f'SELECT COUNT(DISTINCT timeframe) FROM "{table}"')
        info["timeframes"] = cur.fetchone()[0]
        cur.execute(f'SELECT DISTINCT timeframe FROM "{table}" ORDER BY timeframe')
        info["timeframe_list"] = [row[0] for row in cur.fetchall()]

    # Sample rows
    cur.execute(f'SELECT * FROM "{table}" LIMIT 5')
    info["sample"] = cur.fetchall()

    # Duplicates for tick tables
    if table in ["fact_tick", "fact_tick_old"] and time_col:
        try:
            cur.execute(f"""
                SELECT symbol, {time_col}, source_id, COUNT(*)
                FROM \"{table}\"
                GROUP BY symbol, {time_col}, source_id
                HAVING COUNT(*) > 1
                LIMIT 10
            """)
            dupes = cur.fetchall()
            info["duplicates"] = len(dupes)
            info["duplicate_examples"] = dupes
        except Exception:
            pass

    # Invalid OHLC rows
    if table in ["fact_ohlcv", "fact_tick_aggregated"]:
        try:
            cur.execute(f"""
                SELECT COUNT(*) FROM \"{table}\"
                WHERE high < low OR high < open OR high < close
                   OR low > open OR low > close
                   OR open <= 0 OR high <= 0 OR low <= 0 OR close <= 0
            """)
            info["invalid_ohlc"] = cur.fetchone()[0]
        except Exception:
            pass

    # Null counts (for key columns)
    for col in [
        "symbol",
        "timestamp",
        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]:
        if col in info["columns"]:
            try:
                cur.execute(f'SELECT COUNT(*) FROM "{table}" WHERE {col} IS NULL')
                null_count = cur.fetchone()[0]
                if null_count > 0:
                    info["null_counts"][col] = null_count
            except Exception:
                pass

    return info


def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Get all tables
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    tables = [row[0] for row in cur.fetchall()]

    print(f"Found {len(tables)} tables in SQLite database.")
    print("=" * 80)

    report = {}
    for table in tables:
        print(f"Auditing {table}...")
        report[table] = get_table_info(conn, table)

    conn.close()

    # Save report
    with open("sqlite_audit_full_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for table, info in report.items():
        if info["rows"] > 0:
            print(f"\n{table}:")
            print(f"  Rows: {info['rows']:,}")
            print(f"  Time column: {info['time_column']}")
            if info["min_time"]:
                print(f"  Time range: {info['min_time']} -> {info['max_time']}")
            if info["symbols"] > 0:
                print(f"  Symbols: {info['symbols']}")
            if info["timeframes"] > 0:
                print(f"  Timeframes: {info['timeframes']}")
            if info["duplicates"] > 0:
                print(f"  Duplicates: {info['duplicates']} examples")
            if info["invalid_ohlc"] > 0:
                print(f"  Invalid OHLC: {info['invalid_ohlc']}")
            if info["null_counts"]:
                print(f"  Null counts: {info['null_counts']}")

    print("\n" + "=" * 80)
    print("Full report saved to sqlite_audit_full_report.json")


if __name__ == "__main__":
    main()
