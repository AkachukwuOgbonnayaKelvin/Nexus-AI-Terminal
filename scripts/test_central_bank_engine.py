#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import logging

from central_bank_engine.engine import CentralBankEngine

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    print("=" * 60)
    print("RUNNING CENTRAL BANK ENGINE (FULL PIPELINE)")
    print("=" * 60)

    engine = CentralBankEngine()
    result = await engine.run()

    print(f"\nResult: {result['status']}")
    print(f"Events collected: {result['events']}")
    print(f"Events published: {result['published']}")

    print("\nCollector statuses:")
    for name, status in result.get("collector_status", {}).items():
        print(
            f"  {name}: success={status['success_count']}, errors={status['error_count']}"
        )

    print("\n✅ Engine run complete.")


if __name__ == "__main__":
    asyncio.run(main())
