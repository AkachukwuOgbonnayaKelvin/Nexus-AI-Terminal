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
    watch = engine.watch(sym)

    print(f"Macro Bias: {watch.macro_bias}")
    print(f"Context Bias: {watch.context_bias}")
    print(f"Execution Bias: {watch.execution_bias}")
    print(f"Market State: {watch.market_state.value}")
    print(f"Pullback Expected: {watch.pullback_expected}")
    if watch.pullback_zone_low and watch.pullback_zone_high:
        print(
            f"Pullback Zone: {watch.pullback_zone_low:.5f} – {watch.pullback_zone_high:.5f}"
        )
    if watch.atr_value:
        print(f"ATR: {watch.atr_value:.5f}")
    if watch.expected_pullback_atr:
        print(f"Expected ATR Depth: {watch.expected_pullback_atr:.2f} ATR")
    if watch.expected_duration_min and watch.expected_duration_max:
        print(
            f"Expected Duration: {watch.expected_duration_min}–{watch.expected_duration_max} hours"
        )
    print("Confirmation Required:")
    for req in watch.confirmation_required or []:
        print(f"  - {req}")
    print("Conditions Met:")
    for cond in watch.conditions_met or []:
        print(f"  ✅ {cond}")
    print("Conditions Missing:")
    for cond in watch.conditions_missing or []:
        print(f"  ❌ {cond}")
    print(f"Invalidation Level: {watch.invalidation_level}")
    print(f"Confidence: {watch.confidence:.2f}")
    print(f"Status: {watch.status.value}")
    print(f"Interpretation: {watch.interpretation}")
