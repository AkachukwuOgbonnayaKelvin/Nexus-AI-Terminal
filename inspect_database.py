#!/usr/bin/env python3
"""
NDIP Warehouse Database Inspection
"""

import sqlite3
import os

print("=" * 70)
print("NDIP WAREHOUSE DATABASE INSPECTION")
print("=" * 70)

# Find database files
db_files = []
for file in os.listdir("."):
    if file.endswith(".db") or file.endswith(".sqlite"):
        db_files.append(file)

print(f"\nDatabase files found: {db_files}")

# Check each database
for db_file in db_files:
    print(f"\n{'='*50}")
    print(f"DATABASE: {db_file}")
    print("=" * 50)

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\nTables: {[t[0] for t in tables]}")

        # Check each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]

            # Get columns
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            col_names = [c[1] for c in columns]

            print(f"\n  Table: {table_name}")
            print(f"    Records: {count}")
            print(f"    Columns: {col_names}")

            # Show sample if available
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample = cursor.fetchall()
                print(f"    Sample: {sample}")

        conn.close()
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)
