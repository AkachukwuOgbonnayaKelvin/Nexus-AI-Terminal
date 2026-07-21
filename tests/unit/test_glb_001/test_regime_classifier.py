"""
Unit tests for GLB-001 regime classifier
"""

from intelligence.engines.glb_001_market_regime.regime_classifier import (
    RegimeClassifier,
)
from intelligence.engines.glb_001_market_regime.constants import MarketRegime
from intelligence.engines.glb_001_market_regime.schemas import MarketDimension


def test_risk_on_classification():
    """Test RISK_ON classification"""
    classifier = RegimeClassifier()

    dimensions = {
        "risk_sentiment": MarketDimension(
            name="risk_sentiment",
            value=85,
            weight=0.25,
            contribution=21.25,
            direction="BULLISH",
        ),
        "volatility": MarketDimension(
            name="volatility",
            value=15,
            weight=0.15,
            contribution=2.25,
            direction="BULLISH",
        ),
        "macro_growth": MarketDimension(
            name="macro_growth",
            value=75,
            weight=0.10,
            contribution=7.5,
            direction="BULLISH",
        ),
        "liquidity": MarketDimension(
            name="liquidity",
            value=80,
            weight=0.05,
            contribution=4.0,
            direction="BULLISH",
        ),
    }

    regime, score, _ = classifier.classify(dimensions)

    assert regime == MarketRegime.RISK_ON
    assert score > 70


def test_risk_off_classification():
    """Test RISK_OFF classification"""
    classifier = RegimeClassifier()

    dimensions = {
        "risk_sentiment": MarketDimension(
            name="risk_sentiment",
            value=15,
            weight=0.25,
            contribution=3.75,
            direction="BEARISH",
        ),
        "volatility": MarketDimension(
            name="volatility",
            value=85,
            weight=0.15,
            contribution=12.75,
            direction="BEARISH",
        ),
        "macro_growth": MarketDimension(
            name="macro_growth",
            value=20,
            weight=0.10,
            contribution=2.0,
            direction="BEARISH",
        ),
    }

    regime, score, _ = classifier.classify(dimensions)

    assert regime == MarketRegime.RISK_OFF
    assert score > 70


def test_trending_classification():
    """Test TRENDING classification"""
    classifier = RegimeClassifier()

    dimensions = {
        "trend_strength": MarketDimension(
            name="trend_strength",
            value=85,
            weight=0.20,
            contribution=17.0,
            direction="BULLISH",
        ),
        "momentum": MarketDimension(
            name="momentum",
            value=80,
            weight=0.10,
            contribution=8.0,
            direction="BULLISH",
        ),
        "volatility": MarketDimension(
            name="volatility",
            value=20,
            weight=0.15,
            contribution=3.0,
            direction="BULLISH",
        ),
    }

    regime, score, _ = classifier.classify(dimensions)

    assert regime == MarketRegime.TRENDING
    assert score > 60
