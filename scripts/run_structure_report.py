#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
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

with ohlc.engine.connect() as conn:
    result = conn.execute(
        text("SELECT DISTINCT symbol FROM technical_ohlc.bars ORDER BY symbol")
    )
    symbols = [row[0] for row in result]

print(f"=== STRUCTURE REPORT – {len(symbols)} SYMBOLS ===\n")

report_data = []

for sym in symbols:
    try:
        watch = engine.watch(
            sym, timeframes=["D1", "H4", "H1", "M15"], lookback_bars=200
        )
        # Fallback if current price is missing
        current_price = watch.current_price if watch.current_price else None
        row = {
            "Symbol": sym,
            "Macro": watch.macro_bias if watch.macro_bias else "unknown",
            "Context": watch.context_bias if watch.context_bias else "unknown",
            "Execution": watch.execution_bias if watch.execution_bias else "unknown",
            "State": watch.market_state.value if watch.market_state else "unknown",
            "Status": watch.status.value if watch.status else "unknown",
            "Pullback": watch.pullback_expected,
            "Zone Low": watch.pullback_zone_low,
            "Zone High": watch.pullback_zone_high,
            "ATR": watch.atr_value,
            "Current Price": current_price,
            "Distance (ATR)": watch.distance_atr,
            "Time to Zone (h)": f"{watch.time_to_zone_min:.1f}-{watch.time_to_zone_max:.1f}"
            if watch.time_to_zone_min
            else None,
            "Confidence": watch.confidence,
            "Setup ID": watch.setup_id,
        }
        report_data.append(row)
        print(
            f"{sym:12} | {row['Macro']:8} | {row['Context']:8} | {row['Execution']:8} | {row['State']:30} | {row['Status']:20}"
        )
    except Exception as e:
        print(f"{sym:12} | ERROR: {e}")
        # Still add a row with error info
        report_data.append(
            {
                "Symbol": sym,
                "Macro": "ERROR",
                "Context": "",
                "Execution": "",
                "State": str(e)[:30],
                "Status": "FAILED",
                "Pullback": False,
                "Zone Low": None,
                "Zone High": None,
                "ATR": None,
                "Current Price": None,
                "Distance (ATR)": None,
                "Time to Zone (h)": None,
                "Confidence": 0.0,
                "Setup ID": None,
            }
        )

df = pd.DataFrame(report_data)
df.to_csv("structure_report.csv", index=False)
print(f"\nReport saved to structure_report.csv ({len(df)} rows)")
