#!/usr/bin/env python3
"""Run only the COT Engine directly."""

import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import asyncio
import logging

from institutional_positioning_engine.runtime.automated_scheduler import (
    AutomatedCOTScheduler,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def run_cot():
    print("=" * 60)
    print("COT ENGINE ONLY - DIRECT RUN")
    print("=" * 60)

    scheduler = AutomatedCOTScheduler()

    # Run a single cycle
    result = await scheduler.run_once()
    print(f"\nResult: {result}")

    # Show health
    health = scheduler.provider_manager.health_check()
    print(f"\nProvider Health: {health}")

    # Show warehouse stats
    try:
        from ndip.utils.db_connector import fetchrow

        row = await fetchrow("SELECT COUNT(*) FROM cot_reports")
        print(f"\nTotal records in warehouse: {row[0] if row else 0}")
    except Exception as e:
        print(f"Warehouse check: {e}")


if __name__ == "__main__":
    asyncio.run(run_cot())
