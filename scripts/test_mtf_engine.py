import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

symbols = ["EURUSD", "GBPUSD", "XAUUSD"]

for sym in symbols:
    print(f"\n===== {sym} =====")
    result = engine.analyze_mtf(
        sym, timeframes=["D1", "H4", "H1", "M15"], lookback_bars=200
    )

    print(f"Macro Bias: {result.get('macro_bias')}")
    print(f"Context Bias: {result.get('context_bias')}")
    print(f"Execution Bias: {result.get('execution_bias')}")
    print(f"Alignment State: {result.get('alignment_state')}")
    print(f"Weighted Confidence: {result.get('weighted_confidence', 0):.2f}")
    print("Timeframes:")
    for tf, data in result["timeframes"].items():
        print(
            f"  {tf}: bias={data['bias']}, conf={data['confidence']:.2f}, regime={data['regime']}, phase={data['phase']}"
        )
    print(f"Interpretation:\n  {result.get('interpretation')}")
