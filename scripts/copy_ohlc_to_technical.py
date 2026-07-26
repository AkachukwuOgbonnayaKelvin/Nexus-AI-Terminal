import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import psycopg2

from intelligence.technical.stores.ohlc.writer import OHLCWriter

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"
writer = OHLCWriter(DB_CONN)

# ---------- CONFIGURATION ----------
RAW_TABLE = "raw.market_ohlcv"
SYMBOL = "EURUSD"  # You can change to any symbol
TIMEFRAME = "1H"  # Change to "4H", "1D", etc.
LIMIT = 5000  # Last 5000 bars
# ------------------------------------

query = f"""
SELECT
    symbol,
    time,
    open,
    high,
    low,
    close,
    volume
FROM {RAW_TABLE}
WHERE symbol = %s
  AND timeframe = %s
ORDER BY time DESC
LIMIT %s
"""

with psycopg2.connect(DB_CONN) as conn:
    df = pd.read_sql(
        query, conn, params=(SYMBOL, TIMEFRAME, LIMIT), parse_dates=["time"]
    )

if not df.empty:
    writer.write_bars(df, TIMEFRAME)
    print(f"Copied {len(df)} bars from {RAW_TABLE} to technical_ohlc.bars")
else:
    print(f"No data found for {SYMBOL} {TIMEFRAME} in {RAW_TABLE}")
