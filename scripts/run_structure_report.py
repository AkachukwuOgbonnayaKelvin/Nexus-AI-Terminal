#!/usr/bin/env python
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intelligence.technical.stores.ohlc.repository import PostgresOHLCRepository
from intelligence.technical.stores.microstructure.repository import PostgresMicrostructureRepository
from intelligence.technical.data_access import TechnicalDataPlatform
from intelligence.technical.engines.market_structure.engine import MarketStructureEngine
from sqlalchemy import text
import pandas as pd

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

ohlc = PostgresOHLCRepository(DB_CONN)
micro = PostgresMicrostructureRepository(DB_CONN)
platform = TechnicalDataPlatform(ohlc, micro)
engine = MarketStructureEngine(platform)

with ohlc.engine.connect() as conn:
    result = conn.execute(text("SELECT DISTINCT symbol FROM technical_ohlc.bars ORDER BY symbol"))
    symbols = [row[0] for row in result]

print(f"=== STRUCTURE REPORT – {len(symbols)} SYMBOLS ===\n")

report_data = []

for sym in symbols:
    try:
        watch = engine.watch(sym, timeframes=['D1', 'H4', 'H1', 'M15'], lookback_bars=200)
        # Summary
        row = {
            "Symbol": sym,
            "Macro": watch.macro_bias,
            "Context": watch.context_bias,
            "Execution": watch.execution_bias,
            "State": watch.market_state.value,
            "Status": watch.status.value,
            "Pullback": watch.pullback_expected,
            "Zone Low": watch.pullback_zone_low,
            "Zone High": watch.pullback_zone_high,
            "ATR": watch.atr_value,
            "Current Price": watch.current_price,
            "Distance (ATR)": watch.distance_atr,
            "Time to Zone (h)": f"{watch.time_to_zone_min:.1f}-{watch.time_to_zone_max:.1f}" if watch.time_to_zone_min else None,
            "Confidence": watch.confidence,
            "Setup ID": watch.setup_id,
        }
        report_data.append(row)
        # Print symbol with state
        print(f"{sym:12} | {watch.macro_bias:8} | {watch.context_bias:8} | {watch.execution_bias:8} | {watch.market_state.value:30} | {watch.status.value:20}")
    except Exception as e:
        print(f"{sym:12} | ERROR: {e}")

# Optionally save to CSV
df = pd.DataFrame(report_data)
df.to_csv("structure_report.csv", index=False)
print(f"\nReport saved to structure_report.csv ({len(df)} rows)")
