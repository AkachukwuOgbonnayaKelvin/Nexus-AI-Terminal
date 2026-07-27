#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from intelligence.technical.data_access import TechnicalDataPlatform
from intelligence.technical.engines.market_structure.engine import MarketStructureEngine
from intelligence.technical.stores.microstructure.repository import (
    PostgresMicrostructureRepository,
)
from intelligence.technical.stores.ohlc.repository import PostgresOHLCRepository

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

ohlc = PostgresOHLCRepository(DB_CONN)
micro = PostgresMicrostructureRepository(DB_CONN)
platform = TechnicalDataPlatform(ohlc, micro)
engine = MarketStructureEngine(platform)

# Get all distinct symbols from technical_ohlc.bars
with ohlc.engine.connect() as conn:
    result = conn.execute(
        text("SELECT DISTINCT symbol FROM technical_ohlc.bars ORDER BY symbol")
    )
    symbols = [row[0] for row in result]

print(f"Analyzing {len(symbols)} symbols...\n")

for sym in symbols:
    try:
        watch = engine.watch(
            sym, timeframes=["D1", "H4", "H1", "M15"], lookback_bars=200
        )
        print(f"\n===== {sym} =====")
        print(
            f"Macro: {watch.macro_bias} | Context: {watch.context_bias} | Exec: {watch.execution_bias}"
        )
        print(f"State: {watch.market_state.value}")
        print(f"Status: {watch.status.value}")
        if watch.pullback_expected and watch.pullback_zone_low:
            print(
                f"Pullback Zone: {watch.pullback_zone_low:.5f} – {watch.pullback_zone_high:.5f}"
            )
        if watch.current_price:
            print(f"Current Price: {watch.current_price:.5f}")
        if watch.distance_to_zone is not None:
            print(
                f"Distance to Zone: {watch.distance_to_zone:.5f} ({watch.distance_atr:.2f} ATR)"
            )
        if watch.time_to_zone_min is not None:
            print(
                f"Time to Zone: {watch.time_to_zone_min:.1f}–{watch.time_to_zone_max:.1f} hours"
            )
        print(f"Confidence: {watch.confidence:.2f}")
        print(f"Setup ID: {watch.setup_id}")
        # Print conditions summary
        for cat, conds in watch.conditions.items():
            met = [c for c in conds if c.get("met", False)]
            not_met = [c for c in conds if not c.get("met", False)]
            if met:
                print(f"  {cat.upper()}: ✅ " + ", ".join([c["label"] for c in met]))
            if not_met:
                print(
                    f"  {cat.upper()}: ❌ " + ", ".join([c["label"] for c in not_met])
                )
        print(f"Interpretation: {watch.interpretation[:150]}...")
    except Exception as e:
        print(f"Error for {sym}: {e}")
