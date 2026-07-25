import argparse
import json
import os
import time
from datetime import datetime, timedelta

from intelligence.data.common.writer import (
    DataWriter,
)  # <-- Unified writer (PostgreSQL)
from intelligence.data.volume.contracts import CoverageStatus, VolumeRequest
from intelligence.data.volume.coverage.manager import VolumeDataAvailabilityManager
from intelligence.data.volume.sources.mt5_source import MT5VolumeSource

SYMBOLS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCHF",
    "USDCAD",
    "NZDUSD",
    "EURGBP",
    "EURJPY",
    "GBPJPY",
    "AUDJPY",
    "GBPAUD",
    "XAUUSD",
    "XAGUSD",
    "US500",
    "US100",
    "US30",
    "GER40",
    "UK100",
    "JP225",
    "HK50",
    "AU200",
    "CHINA50",
    "FRA40",
    "CL=F",
    "BZ=F",
    "NG=F",
    "COPPER",
    "PLATINUM",
    "PALLADIUM",
    "ALUMINUM",
    "US02Y",
    "US10Y",
    "US30Y",
    "DE10Y",
    "GB10Y",
    "JP10Y",
    "BTCUSD",
    "ETHUSD",
    "SOLUSD",
    "ADAUSD",
    "DOTUSD",
    "LINKUSD",
]
TIMEFRAMES = ["D1", "H4", "H1", "M15", "M5"]

GLOBAL_CHECKPOINT_FILE = "volume_bootstrap_global_checkpoint.json"


def load_global_checkpoint():
    if os.path.exists(GLOBAL_CHECKPOINT_FILE):
        with open(GLOBAL_CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    return {"completed": [], "frozen_target": None}


def save_global_checkpoint(checkpoint):
    with open(GLOBAL_CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f, indent=2, default=str)


def run_volume_bootstrap_fast(
    symbol: str, timeframe: str, days_back: int = 90, frozen_target: datetime = None
):
    mgr = VolumeDataAvailabilityManager()
    now = datetime.utcnow()
    target_start = now - timedelta(days=days_back)
    if frozen_target is None:
        frozen_target = now

    coverage = mgr.get_coverage(symbol, timeframe)
    if (
        coverage.status == CoverageStatus.COMPLETE
        and coverage.latest
        and (frozen_target - coverage.latest).total_seconds() < 3600
    ):
        print(f"  {symbol} {timeframe} already up to date.")
        return 0

    # Determine missing range
    if coverage.is_empty:
        start = target_start
        end = frozen_target
    else:
        if coverage.earliest and coverage.earliest > target_start:
            start = target_start
        else:
            start = coverage.latest or target_start
        end = frozen_target

    if start >= end:
        print(f"  {symbol} {timeframe} no gap to fill.")
        return 0

    print(f"  Fetching {symbol} {timeframe} from {start} to {end}")
    source = MT5VolumeSource()
    writer = DataWriter()  # <-- Writes to PostgreSQL
    req = VolumeRequest(
        symbol=symbol, timeframe=timeframe, start=start, end=end, max_bars=100000
    )
    resp = source.fetch(req)

    if not resp.success:
        print(f"  Error: {resp.error}")
        return 0

    if resp.bar_count == 0:
        print("  No bars returned.")
        return 0

    bars = [
        {
            "symbol": b.symbol,
            "timeframe": b.timeframe,
            "time": b.timestamp.isoformat(),
            "open": b.open,
            "high": b.high,
            "low": b.low,
            "close": b.close,
            "tick_volume": b.tick_volume,
            "real_volume": b.real_volume,
            "source_id": b.source_id,
            "quality_score": b.quality_score,
        }
        for b in resp.bars
    ]
    inserted = writer.write_volume(bars)
    print(f"  Inserted {inserted} bars")
    return inserted


def run_bootstrap_fast(days_back: int = 90):
    checkpoint = load_global_checkpoint()
    completed = checkpoint.get("completed", [])
    frozen_target = datetime.utcnow()
    checkpoint["frozen_target"] = frozen_target.isoformat()

    total = 0
    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            job_id = f"{symbol}_{tf}"
            if job_id in completed:
                print(f"Skipping {job_id} (already completed)")
                continue
            print(f"\nProcessing {job_id}...")
            try:
                inserted = run_volume_bootstrap_fast(
                    symbol, tf, days_back, frozen_target
                )
                total += inserted
                if inserted > 0:
                    completed.append(job_id)
                    checkpoint["completed"] = completed
                    save_global_checkpoint(checkpoint)
            except Exception as e:
                print(f"Error on {job_id}: {e}")
                continue
            time.sleep(0.5)
    print(f"\n✅ Done. Total bars inserted: {total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=90)
    args = parser.parse_args()
    run_bootstrap_fast(days_back=args.days)
