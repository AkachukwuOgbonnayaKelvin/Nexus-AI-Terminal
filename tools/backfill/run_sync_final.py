import argparse
import gc
import json
import os
import time
from datetime import UTC, datetime, timedelta

from intelligence.data.common.writer import DataWriter
from intelligence.data.tick.contracts import TickRequest
from intelligence.data.tick.contracts.coverage import CoverageStatus
from intelligence.data.tick.coverage.manager import DataAvailabilityManager
from intelligence.data.tick.sources import MT5Source

CHECKPOINT_FILE = "tick_sync_checkpoint.json"


def load_checkpoint(symbol: str) -> dict:
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
            return data.get(symbol, {})
    return {}


def save_checkpoint(symbol: str, checkpoint: dict):
    data = {}
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
    data[symbol] = checkpoint
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def run_sync(symbol: str, days_back: int = 3, frozen_target: datetime = None):
    mgr = DataAvailabilityManager()
    now = datetime.now(UTC)
    target_start = now - timedelta(days=days_back)
    if frozen_target is None:
        frozen_target = now

    print(f"\n=== Running sync for {symbol} ===")
    print(f"Target: {target_start} -> {frozen_target} (frozen)")

    plan = mgr.plan_sync(symbol, target_start, frozen_target)
    print(f"Status: {plan.status}")
    print(f"Missing ranges: {len(plan.missing_ranges)}")
    if plan.incremental_range:
        print(
            f"Incremental range: {plan.incremental_range.start} -> {plan.incremental_range.end}"
        )

    if plan.status == CoverageStatus.COMPLETE and not plan.incremental_range:
        print("Already complete.")
        return 0

    source = MT5Source()
    writer = DataWriter()
    total_inserted = 0

    for idx, gap in enumerate(plan.missing_ranges):
        print(f"\n=== Job {idx + 1}: {gap.description} ===")
        print(f"  Gap: {gap.start} -> {gap.end}")
        current = gap.start
        end = gap.end

        checkpoint = load_checkpoint(symbol)
        last_completed = checkpoint.get("last_completed")
        if last_completed:
            last_completed_dt = datetime.fromisoformat(last_completed)
            # Make it timezone-aware (UTC) if it's naive
            if last_completed_dt.tzinfo is None:
                last_completed_dt = last_completed_dt.replace(tzinfo=UTC)
            if last_completed_dt > current and last_completed_dt < end:
                print(f"  Resuming from checkpoint inside gap: {last_completed_dt}")
                # Optionally skip ahead, but we'll start from gap start for safety
                # current = last_completed_dt
            else:
                print("  Checkpoint outside gap, starting from gap start.")

        while current < end:
            window_end = min(current + timedelta(hours=1), end)
            print(f"  Window: {current} -> {window_end}")

            req = TickRequest(
                symbol=symbol, start=current, end=window_end, max_ticks=100000
            )
            resp = source.fetch(req)

            if resp.success and resp.tick_count > 0:
                tick_dicts = [
                    {
                        "symbol": t.symbol,
                        "timestamp": t.timestamp.isoformat(),
                        "bid": t.bid,
                        "ask": t.ask,
                        "last": t.last,
                        "volume": t.volume,
                        "source_id": t.source_id,
                        "quality_score": t.quality_score,
                    }
                    for t in resp.ticks
                ]
                inserted = writer.write_ticks(tick_dicts)
                total_inserted += inserted
                print(f"    Inserted {inserted} (total: {total_inserted})")
                save_checkpoint(
                    symbol,
                    {
                        "last_completed": window_end.isoformat(),
                        "total_inserted": total_inserted,
                        "gap_start": gap.start.isoformat(),
                        "gap_end": gap.end.isoformat(),
                        "symbol": symbol,
                    },
                )
            else:
                print(
                    f"    No ticks or error: {resp.error if not resp.success else 'empty'}"
                )

            current = window_end
            time.sleep(0.5)
            gc.collect()

        save_checkpoint(
            symbol,
            {
                "last_completed": gap.end.isoformat(),
                "total_inserted": total_inserted,
                "gap_complete": True,
                "symbol": symbol,
            },
        )
        print(f"  Job complete. Gap {gap.start} -> {gap.end} fully processed.")

    if plan.incremental_range:
        gap = plan.incremental_range
        print("\n=== Incremental sync ===")
        print(f"  Gap: {gap.start} -> {gap.end}")
        current = gap.start
        end = gap.end

        while current < end:
            window_end = min(current + timedelta(hours=1), end)
            print(f"  Window: {current} -> {window_end}")

            req = TickRequest(
                symbol=symbol, start=current, end=window_end, max_ticks=100000
            )
            resp = source.fetch(req)

            if resp.success and resp.tick_count > 0:
                tick_dicts = [
                    {
                        "symbol": t.symbol,
                        "timestamp": t.timestamp.isoformat(),
                        "bid": t.bid,
                        "ask": t.ask,
                        "last": t.last,
                        "volume": t.volume,
                        "source_id": t.source_id,
                        "quality_score": t.quality_score,
                    }
                    for t in resp.ticks
                ]
                inserted = writer.write_ticks(tick_dicts)
                total_inserted += inserted
                print(f"    Inserted {inserted} (total: {total_inserted})")
                save_checkpoint(
                    symbol,
                    {
                        "last_completed": window_end.isoformat(),
                        "total_inserted": total_inserted,
                        "gap_start": gap.start.isoformat(),
                        "gap_end": gap.end.isoformat(),
                        "symbol": symbol,
                    },
                )
            else:
                print(
                    f"    No ticks or error: {resp.error if not resp.success else 'empty'}"
                )

            current = window_end
            time.sleep(0.5)
            gc.collect()

        save_checkpoint(
            symbol,
            {
                "last_completed": gap.end.isoformat(),
                "total_inserted": total_inserted,
                "gap_complete": True,
                "symbol": symbol,
            },
        )

    final_plan = mgr.plan_sync(symbol, target_start, frozen_target)
    print(f"\nCoverage after sync (frozen target): {final_plan.status}")
    if final_plan.status == CoverageStatus.COMPLETE:
        print("All data up to date for the frozen target!")
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, "r") as f:
                data = json.load(f)
            if symbol in data:
                del data[symbol]
                with open(CHECKPOINT_FILE, "w") as f:
                    json.dump(data, f, indent=2, default=str)
    else:
        print(f"Still missing: {len(final_plan.missing_ranges)} gaps")
        for g in final_plan.missing_ranges:
            print(f"  {g.start} -> {g.end} ({g.description})")

    return total_inserted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="EURUSD")
    parser.add_argument("--days", type=int, default=3)
    args = parser.parse_args()
    run_sync(args.symbol, args.days)
