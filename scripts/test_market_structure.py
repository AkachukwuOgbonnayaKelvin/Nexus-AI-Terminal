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

# Initialize providers
ohlc_repo = PostgresOHLCRepository(DB_CONN)
micro_repo = PostgresMicrostructureRepository(DB_CONN)  # not used yet
data_platform = TechnicalDataPlatform(ohlc_repo, micro_repo)

# Create engine
engine = MarketStructureEngine(data_platform)

# Run analysis
signal = engine.analyze("EURUSD", "H1", lookback_bars=150)

# Print results
print("\n=== Market Structure Analysis ===")
print(f"Symbol: {signal.symbol}")
print(f"Timeframe: {signal.timeframe}")
print(f"Bias: {signal.bias.value}")
print(f"Confidence: {signal.confidence:.2f}")
print(f"Regime: {signal.regime.value} (conf: {signal.regime_confidence:.2f})")
print(f"Invalidation Level: {signal.invalidation_level}")
print(f"Invalidation Condition: {signal.invalidation_condition}")
print("\nKey Levels:")
for lvl in signal.key_levels:
    print(
        f"  {lvl['type'].capitalize()}: {lvl['level']:.5f} (strength: {lvl['strength']:.2f})"
    )
print("\nEvents:")
for evt in signal.events:
    print(f"  {evt['type']} at {evt['level']:.5f}")
print("\nReasoning:")
for r in signal.reasoning:
    print(f"  - {r}")
print(f"\nData Quality: {signal.data_quality:.2f}")
print(f"Bars analyzed: {signal.extras.get('bars_analyzed', 0)}")
