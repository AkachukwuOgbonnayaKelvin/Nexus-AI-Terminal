#!/usr/bin/env python3
"""Test the Metadata Engine with Yahoo provider."""

import asyncio
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ndip.acquisition.metadata_collector import MetadataAcquisitionCollector
from ndip.utils.db_connector import close_pool
from ndip.warehouses.metadata_warehouse import MetadataWarehouse
from providers.provider_manager import ProviderManager
from providers.tier2_secondary.yahoo_metadata import YahooMetadataAdapter, YahooMetadataConnector


async def main():
    print("=" * 60)
    print("TESTING METADATA ENGINE")
    print("=" * 60)

    # 1. Create Provider Manager
    pm = ProviderManager()
    yahoo = YahooMetadataConnector()
    pm.register_provider("yahoo_metadata", yahoo, YahooMetadataAdapter())

    # 2. Create Collector
    collector = MetadataAcquisitionCollector(pm)

    # 3. Collect metadata for a few symbols
    symbols = ["EURUSD", "AAPL", "BTC-USD", "GC=F"]
    print(f"\nCollecting metadata for: {symbols}")
    results = await collector.collect(symbols)

    for symbol, result in results.items():
        print(f"  {symbol}: {result}")

    # 4. Query the warehouse
    warehouse = MetadataWarehouse()
    for symbol in symbols:
        asset = await warehouse.get_asset(symbol)
        if asset:
            print(f"\n{symbol}:")
            print(f"  Asset ID: {asset.get('asset_id')}")
            print(f"  Name: {asset.get('long_name') or asset.get('short_name')}")
            print(f"  Asset Class: {asset.get('asset_class')}")
            print(f"  Exchange: {asset.get('exchange_code')}")
            print(f"  Quality Score: {asset.get('quality_score')}")
            print(f"  Version: {asset.get('version')}")
        else:
            print(f"{symbol}: Not found")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
