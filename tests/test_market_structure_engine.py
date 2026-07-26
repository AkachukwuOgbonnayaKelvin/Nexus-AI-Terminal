from unittest.mock import Mock

import numpy as np
import pandas as pd

from intelligence.technical.contracts import EngineBias
from intelligence.technical.engines.market_structure.engine import MarketStructureEngine


class TestMarketStructureEngine:
    def test_uptrend_detection(self):
        mock = Mock()
        dates = pd.date_range("2024-01-01", periods=100, freq="1H")
        base = 1.0800
        df = pd.DataFrame(
            {
                "time": dates,
                "open": base
                + np.arange(100) * 0.0002
                + np.random.normal(0, 0.0001, 100),
                "high": base
                + np.arange(100) * 0.0002
                + 0.0002
                + np.random.normal(0, 0.0001, 100),
                "low": base
                + np.arange(100) * 0.0002
                - 0.0002
                + np.random.normal(0, 0.0001, 100),
                "close": base
                + np.arange(100) * 0.0002
                + np.random.normal(0, 0.0001, 100),
                "volume": 1000 + np.random.randint(0, 500, 100),
            }
        )
        mock.get_bars.return_value = df
        engine = MarketStructureEngine(mock)
        signal = engine.analyze("EURUSD", "1H")
        assert signal.bias in [EngineBias.BULLISH, EngineBias.NEUTRAL]
        assert signal.confidence > 0.3

    def test_empty_data(self):
        mock = Mock()
        mock.get_bars.return_value = pd.DataFrame()
        engine = MarketStructureEngine(mock)
        signal = engine.analyze("EURUSD", "1H")
        assert signal.bias == EngineBias.UNKNOWN
        assert signal.confidence == 0.0
        assert "Insufficient data" in signal.reasoning[0]
