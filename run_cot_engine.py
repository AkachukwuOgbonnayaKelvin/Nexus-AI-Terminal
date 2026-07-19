#!/usr/bin/env python3
"""INS-001 Market Positioning Warehouse – Complete Run."""

import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncio
import logging

from market_positioning_warehouse.runtime.lifecycle import LifecycleManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def main():
    print("=" * 60)
    print("INS-001 MARKET POSITIONING WAREHOUSE")
    print("INSTITUTIONAL COT DATA PLATFORM")
    print("=" * 60)

    manager = LifecycleManager()
    result = await manager.run()

    print(f"\nMode: {result.get('mode')}")
    print(f"Result: {result.get('result')}")


if __name__ == "__main__":
    asyncio.run(main())
