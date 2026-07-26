"""
Multi‑timeframe aggregator for Market Structure Engine.
Runs the engine on multiple timeframes and aggregates results.
"""

from typing import Dict, List
from intelligence.technical.contracts import EngineBias
from intelligence.technical.engines.market_structure.engine import MarketStructureEngine

class MTFAggregator:
    def __init__(self, engine: MarketStructureEngine):
        self.engine = engine

    def aggregate(self, symbol: str, timeframes: List[str], lookback_bars: int = 200) -> Dict:
        signals = {}
        for tf in timeframes:
            signals[tf] = self.engine.analyze(symbol, tf, lookback_bars=lookback_bars)

        # Determine primary bias from higher timeframes (D1 first, then H4)
        primary_bias = EngineBias.UNKNOWN
        for tf in ['D1', 'H4']:
            if tf in signals and signals[tf].bias != EngineBias.UNKNOWN:
                primary_bias = signals[tf].bias
                break

        # Check alignment: all non‑unknown biases match primary
        aligned = True
        for tf, sig in signals.items():
            if sig.bias != EngineBias.UNKNOWN and sig.bias != primary_bias:
                aligned = False
                break

        return {
            'signals': signals,
            'primary_bias': primary_bias,
            'aligned': aligned
        }
