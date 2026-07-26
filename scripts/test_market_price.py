#!/usr/bin/env python3
"""Test Market Price Engine with new NDIP architecture."""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ndip.acquisition.collector import AcquisitionCollector
from ndip.connectors.yahoo_connector import YahooConnector
from ndip.utils.db_connector import close_pool
from ndip.warehouses.price.warehouse import PriceWarehouse


async def main():
    print("=" * 60)
    print("TESTING MARKET PRICE ENGINE WITH NEW NDIP ARCHITECTURE")
    print("=" * 60)

    # 1. Create collector and register provider
    collector = AcquisitionCollector()
    yahoo = YahooConnector()
    collector.register_provider("yahoo", yahoo)

    # 2. Fetch real data
    print("\n[1] Fetching real data from Yahoo Finance...")
    symbol = "EURUSD"
    data = yahoo.get_price(symbol)
    if not data:
        print("❌ Failed to fetch data")
        return

    print(f"   ✅ Fetched {symbol}: price = {data['value']}")

    # 3. Ingest through NDIP pipeline
    print("\n[2] Ingesting through NDIP pipeline...")
    result = await collector.ingest("yahoo", data)
    if result.get("success"):
        print("   ✅ Ingest successful")
        print(f"      Stored in table: {result.get('record', {}).get('table')}")
    else:
        print(f"   ❌ Ingest failed: {result.get('error')}")

    # 4. Query the warehouse to verify
    print("\n[3] Querying warehouse for stored data...")
    pw = PriceWarehouse()
    records = await pw.query(symbol, limit=5)
    print(f"   Found {len(records)} records for {symbol}")
    for r in records:
        print(f"      {r['time']}: {r['price']}")

    # 5. Close connection pool
    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
