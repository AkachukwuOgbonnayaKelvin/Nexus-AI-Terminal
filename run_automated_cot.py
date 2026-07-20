#!/usr/bin/env python3
"""Fully Automated COT Engine – Institutional Grade."""

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


async def main():
    print("=" * 60)
    print("INS-001 INSTITUTIONAL POSITIONING ENGINE")
    print("FULLY AUTOMATED – INSTITUTIONAL GRADE")
    print("=" * 60)

    scheduler = AutomatedCOTScheduler()
    try:
        await scheduler.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
