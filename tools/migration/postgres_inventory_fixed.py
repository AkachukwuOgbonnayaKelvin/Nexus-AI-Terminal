import os

import psycopg2

PGPASSWORD = os.getenv("PGPASSWORD", "6468")
conn = psycopg2.connect(
    f"dbname=nexus_ai_terminal user=postgres password={PGPASSWORD} host=localhost"
)
cur = conn.cursor()
conn.autocommit = True  # Prevent transaction issues

# Get all schemas
cur.execute("""
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast', '_timescaledb_cache', '_timescaledb_config', '_timescaledb_catalog', '_timescaledb_internal')
    ORDER BY schema_name;
""")
schemas = [row[0] for row in cur.fetchall()]

print("=" * 80)
print("POSTGRESQL DATABASE INVENTORY")
print("=" * 80)

total_tables = 0
total_rows = 0
total_size_bytes = 0

for schema in schemas:
    cur.execute(f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{schema}'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cur.fetchall()]
    if not tables:
        continue
    print(f"\nSCHEMA: {schema} ({len(tables)} tables)")
    print("-" * 80)
    for table in tables:
        try:
            # Count rows
            cur.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
            count = cur.fetchone()[0]
            total_rows += count
            total_tables += 1
            # Get size
            cur.execute(f"""
                SELECT pg_size_pretty(pg_total_relation_size('{schema}.{table}'));
            """)
            size = cur.fetchone()[0]
            # Try to get time range if time column exists
            time_range = ""
            try:
                cur.execute(f"""
                    SELECT MIN(time), MAX(time) FROM {schema}.{table}
                """)
                row = cur.fetchone()
                if row and row[0] and row[1]:
                    time_range = f" ({row[0]} to {row[1]})"
            except Exception:
                # Try timestamp column
                try:
                    cur.execute(f"""
                        SELECT MIN(timestamp), MAX(timestamp) FROM {schema}.{table}
                    """)
                    row = cur.fetchone()
                    if row and row[0] and row[1]:
                        time_range = f" ({row[0]} to {row[1]})"
                except Exception:
                    pass
            print(f"  {table}: {count:,} rows{time_range} (size: {size})")
        except Exception as e:
            print(f"  {table}: ERROR - {e}")

print("\n" + "=" * 80)
print(f"TOTAL TABLES: {total_tables}")
print(f"TOTAL ROWS: {total_rows:,}")
print("=" * 80)

conn.close()
