import sqlite3

DB = "nexus_data.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

tables = cur.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""").fetchall()

print(f"TOTAL TABLES: {len(tables)}")
print("=" * 100)

for (table,) in tables:
    print(f"\nTABLE: {table}")

    columns = cur.execute(f'PRAGMA table_info("{table}")').fetchall()

    print("COLUMNS:")
    for col in columns:
        print(f"  {col[1]} | {col[2]} | nullable={not col[3]}")

    count = cur.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]

    print(f"ROWS: {count:,}")

conn.close()
