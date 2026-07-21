# -*- coding: utf-8 -*-
"""ECO-002 Runtime Scheduler - Called by Central Scheduler"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def run_eco002():
    """Run ECO-002 corporate earnings acquisition"""
    print("[ECO-002] Running corporate earnings acquisition...")

    try:
        from corporate_earnings_engine.collectors.earnings_collector import (
            EarningsCollector,
        )

        collector = EarningsCollector()

        # Test with a few symbols
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        observations = collector.collect(symbols)

        print(f"[ECO-002] Earnings: {len(observations)} observations")

        # Group by symbol
        symbols_data = {}
        for obs in observations:
            if obs.symbol not in symbols_data:
                symbols_data[obs.symbol] = []
            symbols_data[obs.symbol].append(obs)

        for symbol, obs_list in symbols_data.items():
            print(f"[ECO-002]   {symbol}: {len(obs_list)} earnings records")

        print("[ECO-002] Corporate earnings acquisition complete")
        return {
            "status": "SUCCESS",
            "earnings": len(observations),
            "symbols": len(symbols_data),
        }

    except Exception as e:
        print(f"[ECO-002] Error: {e}")
        return {"status": "FAILED", "error": str(e)}


def run_eco002_symbol(symbol: str):
    """Run ECO-002 for a specific symbol"""
    print(f"[ECO-002] Running earnings acquisition for {symbol}...")

    try:
        from corporate_earnings_engine.collectors.earnings_collector import (
            EarningsCollector,
        )

        collector = EarningsCollector()
        observations = collector._collect_for_symbol(symbol)

        print(f"[ECO-002] {symbol}: {len(observations)} earnings records")
        return {"status": "SUCCESS", "symbol": symbol, "count": len(observations)}

    except Exception as e:
        print(f"[ECO-002] Error: {e}")
        return {"status": "FAILED", "error": str(e)}
