import argparse
import json
import os
import time
from datetime import datetime, timedelta

from intelligence.data.tick.contracts.coverage import CoverageStatus  # Fixed
from run_sync_final import run_sync

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

GLOBAL_CHECKPOINT_FILE = "tick_sync_global_checkpoint.json"


def load_global_checkpoint():
    if os.path.exists(GLOBAL_CHECKPOINT_FILE):
        with open(GLOBAL_CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    return {"completed": [], "frozen_target": None}


def save_global_checkpoint(checkpoint):
    with open(GLOBAL_CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f, indent=2, default=str)


def run_all(days_back: int = 3, symbols: list = None):
    if symbols is None:
        symbols = SYMBOLS

    frozen_target = datetime.utcnow()
    print(f"=== Running sync for {len(symbols)} symbols ===")
    print(f"Frozen target: {frozen_target}")
    print(f"Days back: {days_back}\n")

    global_checkpoint = load_global_checkpoint()
    completed = global_checkpoint.get("completed", [])

    stored_target = global_checkpoint.get("frozen_target")
    if stored_target:
        stored_target_dt = datetime.fromisoformat(stored_target)
        if abs((frozen_target - stored_target_dt).total_seconds()) > 60:
            print(
                "Frozen target has changed significantly, resetting global checkpoint."
            )
            completed = []
            global_checkpoint["completed"] = []
        else:
            print(
                f"Resuming from global checkpoint. Completed: {len(completed)} symbols"
            )
    else:
        print("No global checkpoint found. Starting fresh.")

    global_checkpoint["frozen_target"] = frozen_target.isoformat()
    save_global_checkpoint(global_checkpoint)

    total_inserted_all = 0
    for idx, symbol in enumerate(symbols):
        if symbol in completed:
            print(
                f"\n[{idx + 1}/{len(symbols)}] {symbol} - already completed, skipping."
            )
            continue

        print(f"\n[{idx + 1}/{len(symbols)}] {symbol} - starting sync...")
        try:
            inserted = run_sync(
                symbol, days_back=days_back, frozen_target=frozen_target
            )
            total_inserted_all += inserted

            from intelligence.data.tick.coverage.manager import DataAvailabilityManager

            mgr = DataAvailabilityManager()
            now = datetime.utcnow()
            target_start = now - timedelta(days=days_back)
            plan = mgr.plan_sync(symbol, target_start, frozen_target)
            if plan.status == CoverageStatus.COMPLETE:
                completed.append(symbol)
                global_checkpoint["completed"] = completed
                save_global_checkpoint(global_checkpoint)
                print(f"  ✅ {symbol} complete.")
            else:
                print(f"  ⚠️ {symbol} not complete after sync, will retry on next run.")
        except KeyboardInterrupt:
            print("\nInterrupted. Saving progress...")
            save_global_checkpoint(global_checkpoint)
            raise
        except Exception as e:
            print(f"  ❌ Error syncing {symbol}: {e}")
            save_global_checkpoint(global_checkpoint)
            continue

        time.sleep(2)

    print(f"\n✅ All symbols processed. Total inserted: {total_inserted_all}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=3, help="Days back to sync")
    parser.add_argument(
        "--symbols", type=str, help="Comma-separated list of symbols (optional)"
    )
    args = parser.parse_args()

    symbols = None
    if args.symbols:
        symbols = [s.strip() for s in args.symbols.split(",")]

    run_all(days_back=args.days, symbols=symbols)
