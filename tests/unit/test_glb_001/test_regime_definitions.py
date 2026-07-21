"""
Unit tests for GLB-001 regime definitions
"""

from intelligence.engines.glb_001_market_regime.constants import (
    MarketRegime,
    TransitionState,
    RegimeAlignment,
)


def test_market_regime_values():
    """Test that all market regime values are defined"""
    assert MarketRegime.RISK_ON.value == "RISK_ON"
    assert MarketRegime.RISK_OFF.value == "RISK_OFF"
    assert MarketRegime.TRENDING.value == "TRENDING"
    assert MarketRegime.RANGING.value == "RANGING"
    assert MarketRegime.TRANSITION.value == "TRANSITION"
    assert MarketRegime.VOLATILE.value == "VOLATILE"


def test_transition_state_values():
    """Test that all transition state values are defined"""
    assert TransitionState.STABLE.value == "STABLE"
    assert TransitionState.WEAKENING.value == "WEAKENING"
    assert TransitionState.STRENGTHENING.value == "STRENGTHENING"
    assert TransitionState.REVERSING.value == "REVERSING"


def test_regime_alignment_values():
    """Test that all regime alignment values are defined"""
    assert RegimeAlignment.STRONGLY_SUPPORTIVE.value == "STRONGLY_SUPPORTIVE"
    assert RegimeAlignment.SUPPORTIVE.value == "SUPPORTIVE"
    assert RegimeAlignment.NEUTRAL.value == "NEUTRAL"
    assert RegimeAlignment.NEGATIVE.value == "NEGATIVE"
    assert RegimeAlignment.STRONGLY_NEGATIVE.value == "STRONGLY_NEGATIVE"
    assert RegimeAlignment.MIXED.value == "MIXED"
