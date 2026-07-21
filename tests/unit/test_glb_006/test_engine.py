"""
Unit tests for GLB-006 Geopolitical Risk Engine
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime  # noqa: E402
from intelligence.engines.glb_006_geopolitical_risk.engine import GeopoliticalRiskEngine  # noqa: E402
from intelligence.engines.glb_006_geopolitical_risk.constants import NDIP_TOPICS  # noqa: E402


def test_engine_initialization():
    """Test that the engine initializes correctly"""
    engine = GeopoliticalRiskEngine()
    assert engine is not None
    assert engine.last_report is None
    assert engine.last_run_time is None


def test_engine_consume_ndip():
    """Test NDIP consumption"""
    engine = GeopoliticalRiskEngine()
    test_payload = {"events": []}
    engine.consume_ndip("test.topic", test_payload)
    assert engine._latest_data is not None


def test_engine_run_with_data():
    """Test engine run with valid data"""
    engine = GeopoliticalRiskEngine()

    test_events = {
        "events": [
            {
                "event_id": "GEO-001",
                "event_type": "MILITARY_CONFLICT",
                "headline": "Military escalation",
                "countries": ["SA", "IR"],
                "region": "MIDDLE_EAST",
                "severity": 85.0,
                "escalation_probability": 80.0,
                "strategic_importance": 90.0,
                "economic_exposure": 85.0,
                "market_sensitivity": 90.0,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "INTEL",
                "confidence": 88.0,
            }
        ]
    }

    engine.consume_ndip(NDIP_TOPICS["GEOPOLITICAL_EVENTS"], test_events)
    report = engine.run()

    core = report.get("core_intelligence", {})
    assert core.get("global_geopolitical_risk", 0) > 0
    assert core.get("risk_state") is not None

    matrix = report.get("asset_impact_matrix")
    assert matrix is not None
    impacts = matrix.get("impacts", {})
    assert len(impacts) > 0


def test_engine_health_check():
    """Test health check"""
    engine = GeopoliticalRiskEngine()
    health = engine.health_check()

    assert health["engine_id"] == "GLB-006"
    assert health["status"] == "OPERATIONAL"


def test_asset_impact_scores():
    """Test that asset impact scores are in range"""
    engine = GeopoliticalRiskEngine()

    test_events = {
        "events": [
            {
                "event_id": "GEO-001",
                "event_type": "MILITARY_CONFLICT",
                "headline": "Military escalation",
                "countries": ["SA", "IR"],
                "region": "MIDDLE_EAST",
                "severity": 85.0,
                "escalation_probability": 80.0,
                "strategic_importance": 90.0,
                "economic_exposure": 85.0,
                "market_sensitivity": 90.0,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "INTEL",
                "confidence": 88.0,
            }
        ]
    }

    engine.consume_ndip(NDIP_TOPICS["GEOPOLITICAL_EVENTS"], test_events)
    report = engine.run()

    matrix = report.get("asset_impact_matrix")
    impacts = matrix.get("impacts", {})

    for asset, impact in impacts.items():
        score = impact.get("score", 0)
        assert -100 <= score <= 100
        direction = impact.get("direction", "NEUTRAL")
        assert direction in ["BULLISH", "BEARISH", "NEUTRAL"]


def test_risk_score_passing():
    """Test that risk score is properly passed to asset impact"""
    engine = GeopoliticalRiskEngine()

    test_events = {
        "events": [
            {
                "event_id": "GEO-001",
                "event_type": "MILITARY_CONFLICT",
                "headline": "Military escalation",
                "countries": ["SA", "IR"],
                "region": "MIDDLE_EAST",
                "severity": 85.0,
                "escalation_probability": 80.0,
                "strategic_importance": 90.0,
                "economic_exposure": 85.0,
                "market_sensitivity": 90.0,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "INTEL",
                "confidence": 88.0,
            }
        ]
    }

    engine.consume_ndip(NDIP_TOPICS["GEOPOLITICAL_EVENTS"], test_events)
    report = engine.run()

    core = report.get("core_intelligence", {})
    risk_score = core.get("global_geopolitical_risk", 0)

    # Check that at least one asset has a non-zero score
    matrix = report.get("asset_impact_matrix")
    impacts = matrix.get("impacts", {})
    non_zero = [a for a, i in impacts.items() if abs(i.get("score", 0)) > 1]

    assert len(non_zero) > 0, "No assets have non-zero impact scores"
    assert risk_score > 0, "Risk score should be positive"
