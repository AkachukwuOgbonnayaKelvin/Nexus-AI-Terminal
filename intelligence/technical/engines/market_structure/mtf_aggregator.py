from typing import Dict, List
from intelligence.technical.contracts import EngineBias
from intelligence.technical.engines.market_structure.engine import MarketStructureEngine

class MTFAggregator:
    def __init__(self, engine: MarketStructureEngine):
        self.engine = engine

    def aggregate(self, symbol: str, timeframes: List[str], lookback_bars: int = 200) -> Dict:
        signals = {}
        for tf in timeframes:
            try:
                sig = self.engine.analyze(symbol, tf, lookback_bars=lookback_bars)
                if sig is not None:
                    # Include all signals, even if data quality is insufficient.
                    # The MTF state classifier will handle the quality status.
                    signals[tf] = sig
            except Exception as e:
                # If analysis fails, skip this timeframe
                continue

        if not signals:
            return {'signals': {}, 'primary_bias': EngineBias.UNKNOWN, 'aligned': False}

        primary_bias = EngineBias.UNKNOWN
        for tf in ['D1', 'H4']:
            if tf in signals and signals[tf].bias != EngineBias.UNKNOWN:
                primary_bias = signals[tf].bias
                break

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
