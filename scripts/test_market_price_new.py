#!/usr/bin/env python3
"""Test the new Market Price Engine with ProviderManager."""

import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ndip.engines.market_price import MarketPriceEngine
from ndip.utils.db_connector import close_pool
from providers.provider_manager import ProviderManager
from providers.tier2_secondary.yahoo import YahooAdapter, YahooConnector


async def main():
    print("=" * 60)
    print("TESTING NEW MARKET PRICE ENGINE WITH PROVIDER MANAGER")
    print("=" * 60)

    # 1. Create Provider Manager
    print("\n[1] Initializing Provider Manager...")
    pm = ProviderManager()

    # 2. Register Yahoo provider
    print("[2] Registering Yahoo provider...")
    yahoo = YahooConnector()
    yahoo_adapter = YahooAdapter()
    pm.register_provider("yahoo", yahoo, yahoo_adapter)

    # 3. Create Engine
    print("[3] Creating Market Price Engine...")
    engine = MarketPriceEngine(pm)
    engine.set_symbols(["EURUSD", "AAPL", "BTC-USD"])
    engine.set_interval(10)  # 10 seconds for test

    # 4. Run one collection
    print("[4] Running one collection cycle...")
    results = await engine.collect_once()

    for symbol, result in results.items():
        if result.get("success"):
            print(f"   ✅ {symbol}: {result}")
        else:
            print(f"   ❌ {symbol}: {result.get('error')}")

    # 5. Verify data in warehouse
    print("\n[5] Querying Price Warehouse...")
    from ndip.warehouses.price.warehouse import PriceWarehouse

    pw = PriceWarehouse()
    for symbol in ["EURUSD", "AAPL", "BTC-USD"]:
        records = await pw.query(symbol, limit=3)
        print(f"   {symbol}: {len(records)} records")
        for r in records[:1]:
            print(f"      {r['time']}: {r['price']}")

    await close_pool()
    print("\n✅ Test complete.")


if __name__ == "__main__":
    asyncio.run(main())
