import gc
import json
import os
import time
from datetime import datetime, timedelta

from intelligence.data.tick.contracts import TickRequest
from intelligence.data.tick.contracts.coverage import CoverageStatus
from intelligence.data.tick.coverage.manager import DataAvailabilityManager
from intelligence.data.tick.persistence.sqlite_writer import TickSQLiteWriter
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


def run_sync_plan(symbol: str, days_back: int = 3):
    mgr = DataAvailabilityManager()
    now = datetime.utcnow()
    target_start = now - timedelta(days=days_back)

    plan = mgr.plan_sync(symbol, target_start, now)
    print(f"=== Running sync plan for {symbol} ===")
    print(f"Status: {plan.status}")
    print(f"Jobs: {len(plan.missing_ranges) + (1 if plan.incremental_range else 0)}")

    source = MT5Source()
    writer = TickSQLiteWriter()

    # Load checkpoint
    checkpoint = load_checkpoint(symbol)
    last_completed = checkpoint.get("last_completed")
    if last_completed:
        last_completed = datetime.fromisoformat(last_completed)
        print(f"Resuming from checkpoint: {last_completed}")

    total_inserted = checkpoint.get("total_inserted", 0)

    # Process historical gaps (bootstrap)
    for idx, gap in enumerate(plan.missing_ranges):
        if "Historical" in gap.description:
            print(f"\n=== Running job_{idx:04d}: bootstrap ===")
            current = gap.start
            end = gap.end

            # If we have a checkpoint, resume from there
            if last_completed and last_completed > current:
                current = last_completed
                print(f"  Resuming from {current}")

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
                    inserted = writer.write_fact_tick(tick_dicts)
                    total_inserted += inserted
                    print(f"    Inserted {inserted} (total: {total_inserted})")

                    # Save checkpoint after each successful window
                    save_checkpoint(
                        symbol,
                        {
                            "last_completed": window_end.isoformat(),
                            "total_inserted": total_inserted,
                            "job_type": "bootstrap",
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

            print(f"  Bootstrap complete. Total inserted: {total_inserted}")

    # Process incremental gap (recent data)
    if plan.incremental_range:
        print("\n=== Running job_incremental: incremental sync ===")
        gap = plan.incremental_range
        current = gap.start
        end = gap.end

        # If we have a checkpoint for incremental
        if last_completed and last_completed > current:
            current = last_completed
            print(f"  Resuming from {current}")

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
                inserted = writer.write_fact_tick(tick_dicts)
                total_inserted += inserted
                print(f"    Inserted {inserted} (total: {total_inserted})")

                save_checkpoint(
                    symbol,
                    {
                        "last_completed": window_end.isoformat(),
                        "total_inserted": total_inserted,
                        "job_type": "incremental",
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

        print(f"  Incremental sync complete. Total inserted: {total_inserted}")

    # Re-check coverage after sync
    new_plan = mgr.plan_sync(symbol, target_start, now)
    print(f"\nCoverage after sync: {new_plan.status}")
    if new_plan.status == CoverageStatus.COMPLETE:
        print("✅ All data up to date!")
        # Clear checkpoint when complete
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, "r") as f:
                data = json.load(f)
            if symbol in data:
                del data[symbol]
                with open(CHECKPOINT_FILE, "w") as f:
                    json.dump(data, f, indent=2, default=str)
    else:
        print(f"⚠️ Still missing: {len(new_plan.missing_ranges)} gaps")


if __name__ == "__main__":
    run_sync_plan("EURUSD", days_back=3)
