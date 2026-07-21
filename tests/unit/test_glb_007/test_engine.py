"""
Unit tests for GLB-007 Capital Flows Engine
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest  # noqa: E402
from datetime import datetime  # noqa: E402
from intelligence.engines.glb_007_capital_flows.engine import CapitalFlowsEngine  # noqa: E402
from intelligence.engines.glb_007_capital_flows.constants import NDIP_TOPICS  # noqa: E402


def test_engine_initialization():
    """Test that the engine initializes correctly"""
    engine = CapitalFlowsEngine()
    assert engine is not None
    assert engine.last_report is None
    assert engine.last_run_time is None


def test_engine_consume_ndip():
    """Test NDIP consumption"""
    engine = CapitalFlowsEngine()
    test_payload = {"flows": []}
    engine.consume_ndip("test.topic", test_payload)
    assert engine._latest_data is not None


def test_engine_run_with_data():
    """Test engine run with valid data"""
    engine = CapitalFlowsEngine()
    
    test_data = {
        'flows': [
            {
                'flow_id': 'FLOW-001',
                'asset': 'XAUUSD',
                'region': 'GLOBAL',
                'flow_type': 'SAFE_HAVEN',
                'direction': 'INFLOW',
                'amount': 1250000000,
                'amount_normalized': 85.0,
                'velocity': 82.0,
                'persistence': 74.0,
                'confidence': 88.0,
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'NDIP'
            }
        ]
    }
    liquidity_data = {
        'global_liquidity': 64.5,
        'central_bank_liquidity': 72.0,
        'money_market_liquidity': 61.0,
        'credit_liquidity': 58.0,
        'funding_stress': 32.0,
        'confidence': 82.0,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    engine.consume_ndip(NDIP_TOPICS['CAPITAL_FLOWS'], test_data)
    engine.consume_ndip(NDIP_TOPICS['GLOBAL_LIQUIDITY'], liquidity_data)
    report = engine.run()
    
    core = report.get('core_intelligence', {})
    assert core.get('capital_flow_score', 0) > 0
    assert core.get('flow_direction') is not None
    
    matrix = report.get('asset_impact_matrix')
    assert matrix is not None
    impacts = matrix.get('impacts', {})
    assert len(impacts) > 0


def test_engine_health_check():
    """Test health check"""
    engine = CapitalFlowsEngine()
    health = engine.health_check()
    
    assert health["engine_id"] == "GLB-007"
    assert health["status"] == "OPERATIONAL"


def test_asset_impact_scores():
    """Test that asset impact scores are in range"""
    engine = CapitalFlowsEngine()
    
    test_data = {
        'flows': [
            {
                'flow_id': 'FLOW-001',
                'asset': 'XAUUSD',
                'region': 'GLOBAL',
                'flow_type': 'SAFE_HAVEN',
                'direction': 'INFLOW',
                'amount_normalized': 85.0,
                'confidence': 88.0,
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'NDIP'
            }
        ]
    }
    liquidity_data = {
        'global_liquidity': 64.5,
        'funding_stress': 32.0,
        'confidence': 82.0,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    engine.consume_ndip(NDIP_TOPICS['CAPITAL_FLOWS'], test_data)
    engine.consume_ndip(NDIP_TOPICS['GLOBAL_LIQUIDITY'], liquidity_data)
    report = engine.run()
    
    matrix = report.get('asset_impact_matrix')
    impacts = matrix.get('impacts', {})
    
    for asset, impact in impacts.items():
        score = impact.get('score', 0)
        assert -100 <= score <= 100
        direction = impact.get('direction', 'NEUTRAL')
        assert direction in ['BULLISH', 'BEARISH', 'NEUTRAL']
