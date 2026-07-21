"""
Unit tests for GLB-001 Market Regime Engine
"""

from datetime import datetime
from intelligence.engines.glb_001_market_regime.engine import MarketRegimeEngine
from intelligence.engines.glb_001_market_regime.constants import NDIP_TOPICS


def test_engine_initialization():
    """Test that the engine initializes correctly"""
    engine = MarketRegimeEngine()
    assert engine is not None
    assert engine.last_report is None
    assert engine.last_run_time is None


def test_engine_consume_ndip():
    """Test NDIP consumption"""
    engine = MarketRegimeEngine()
    test_payload = {"test": "data"}
    engine.consume_ndip("test.topic", test_payload)
    assert engine.input_normalizer.last_consumed_at is not None


def test_engine_run_missing_data():
    """Test engine run with missing data"""
    engine = MarketRegimeEngine()
    report = engine.run()
    assert report.metadata.get("error") == "MISSING_DATA"


def test_engine_run_with_data():
    """Test engine run with valid data"""
    engine = MarketRegimeEngine()

    # Provide required data
    engine.consume_ndip(
        NDIP_TOPICS["PRICE_SNAPSHOT"],
        {
            "symbols": {"US500": {"close": 5200, "change_20d": 0.05}},
            "timestamp": datetime.utcnow().isoformat(),
        },
    )
    engine.consume_ndip(
        NDIP_TOPICS["TREND_SNAPSHOT"], {"direction": "BULLISH", "strength": 75}
    )
    engine.consume_ndip(NDIP_TOPICS["VOLATILITY_SNAPSHOT"], {"vix": 14.2, "atr": 0.5})

    report = engine.run()

    assert report.primary_regime is not None
    assert report.regime_score >= 0
    assert report.regime_score <= 100
    assert report.confidence >= 0
    assert report.confidence <= 100


def test_engine_health_check():
    """Test health check"""
    engine = MarketRegimeEngine()
    health = engine.health_check()

    assert health["engine_id"] == "GLB-001"
    assert health["status"] == "OPERATIONAL"
    assert "last_run" in health
    assert "has_report" in health
    assert "ready" in health


def test_engine_report_format():
    """Test that the engine produces the correct report format"""
    engine = MarketRegimeEngine()

    engine.consume_ndip(
        NDIP_TOPICS["PRICE_SNAPSHOT"],
        {
            "symbols": {"US500": {"close": 5200, "change_20d": 0.05}},
            "timestamp": datetime.utcnow().isoformat(),
        },
    )
    engine.consume_ndip(
        NDIP_TOPICS["TREND_SNAPSHOT"], {"direction": "BULLISH", "strength": 75}
    )
    engine.consume_ndip(NDIP_TOPICS["VOLATILITY_SNAPSHOT"], {"vix": 14.2})

    report = engine.run()

    # Check all required fields
    assert hasattr(report, "engine_id")
    assert report.engine_id == "GLB-001"
    assert hasattr(report, "engine_name")
    assert hasattr(report, "primary_regime")
    assert hasattr(report, "regime_score")
    assert hasattr(report, "confidence")
    assert hasattr(report, "dimensions")
    assert hasattr(report, "signals")
    assert hasattr(report, "evidence")
    assert hasattr(report, "risks")
    assert hasattr(report, "drivers")
    assert hasattr(report, "asset_context")
