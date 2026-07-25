#!/usr/bin/env python3
"""
Check Prices Table
"""

import os
import sqlite3

print("=" * 70)
print("PRICES TABLE INSPECTION")
print("=" * 70)

# Find database
db_path = "nexus_data.db"
if not os.path.exists(db_path):
    for file in os.listdir("."):
        if file.endswith(".db"):
            db_path = file
            break

print(f"\nUsing database: {db_path}")

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if prices table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='prices'"
        )
        if cursor.fetchone():
            print("\nPrices table found")

            # Get count
            cursor.execute("SELECT COUNT(*) FROM prices")
            count = cursor.fetchone()[0]
            print(f"  Total records: {count}")

            # Get unique symbols
            cursor.execute("SELECT DISTINCT symbol FROM prices")
            symbols = cursor.fetchall()
            symbol_list = [s[0] for s in symbols]
            print(f"  Symbols ({len(symbol_list)}): {symbol_list[:10]}...")

            # Get date range
            cursor.execute("SELECT MIN(time), MAX(time) FROM prices")
            date_range = cursor.fetchone()
            if date_range:
                print(f"  Date range: {date_range[0]} to {date_range[1]}")

            # Get columns
            cursor.execute("PRAGMA table_info(prices)")
            columns = cursor.fetchall()
            col_names = [c[1] for c in columns]
            print(f"  Columns: {col_names}")

            # Check volume
            if "volume" in col_names:
                cursor.execute(
                    "SELECT COUNT(*) FROM prices WHERE volume IS NOT NULL AND volume > 0"
                )
                volume_count = cursor.fetchone()[0]
                print(f"  Volume records: {volume_count} / {count}")
            else:
                print("  No volume column")

            # Show sample
            cursor.execute("SELECT * FROM prices LIMIT 5")
            sample = cursor.fetchall()
            print("\nSample data:")
            for row in sample:
                print(f"  {row}")

        else:
            print("\nPrices table not found")

            # Show all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"Available tables: {[t[0] for t in tables]}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Database not found: {db_path}")

print("\n" + "=" * 70)
