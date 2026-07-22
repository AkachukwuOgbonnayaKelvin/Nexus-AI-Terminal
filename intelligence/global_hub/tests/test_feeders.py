# -*- coding: utf-8 -*-
"""
Phase 7.7 & 7.8: GUI & Orchestrator Feeders - Integration Test

Tests the final two feeders:
1. GUI Presentation Feeder -> Dashboard
2. Orchestrator Feeder -> Master Orchestrator
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from intelligence.confluence.contracts import (
    GlobalIntelligenceOutput,
    GlobalEntityRating,
    AssetClassRating,
    EntityType,
    Direction,
    AssetClass,
)
from intelligence.global_hub import (
    StateManager,
    IngestionGateway,
    GUIPresentationFeeder,
    OrchestratorFeeder,
)


def create_test_output() -> GlobalIntelligenceOutput:
    """Create test GlobalIntelligenceOutput."""
    entity_ratings = [
        GlobalEntityRating(
            entity="USD",
            entity_type=EntityType.CURRENCY,
            score=84.0,
            direction=Direction.BULLISH,
            confidence=86.5,
            rank=1,
        ),
        GlobalEntityRating(
            entity="JPY",
            entity_type=EntityType.CURRENCY,
            score=74.0,
            direction=Direction.BULLISH,
            confidence=82.0,
            rank=2,
        ),
        GlobalEntityRating(
            entity="AUD",
            entity_type=EntityType.CURRENCY,
            score=-24.0,
            direction=Direction.BEARISH,
            confidence=72.0,
            rank=5,
        ),
    ]

    asset_class_ratings = [
        AssetClassRating(
            asset_class=AssetClass.METALS,
            name="Metals",
            score=81.0,
            direction=Direction.BULLISH,
            confidence=84.0,
            rank=1,
        ),
        AssetClassRating(
            asset_class=AssetClass.EQUITIES,
            name="Equities",
            score=-63.0,
            direction=Direction.BEARISH,
            confidence=78.0,
            rank=5,
        ),
    ]

    return GlobalIntelligenceOutput(
        global_regime="RISK_OFF",
        global_regime_confidence=86.0,
        global_risk_level="HIGH",
        global_risk_score=45.0,
        currency_rankings=entity_ratings,
        entity_rankings=entity_ratings,
        asset_class_rankings=asset_class_ratings,
        global_drivers=["RISK_OFF", "SAFE_HAVEN", "USD_STRENGTH"],
        global_risks=[],
        dominant_themes=[],
        top_opportunities=[],
        executive_summary="Global markets remain risk-off.",
        timestamp=datetime.utcnow(),
    )


def test_feeders():
    """Test both feeders."""

    print("=" * 70)
    print("PHASE 7.7 & 7.8: GUI & ORCHESTRATOR FEEDERS")
    print("=" * 70)

    # Create state
    print("\n[1] Creating State...")
    gateway = IngestionGateway()
    output = create_test_output()
    gateway.ingest(output)

    manager = StateManager()
    state = manager.build_state(output)
    print(f"  State created: {state.state_id}")

    # Test GUI Feeder
    print("\n[2] Testing GUI Presentation Feeder...")
    gui_feeder = GUIPresentationFeeder()
    gui_feed = gui_feeder.prepare_feed(state)

    print("  GUI Feed prepared:")
    print(f"    Overview: {gui_feed['overview']['regime']}")
    print(f"    Currencies: {gui_feed['currency_intelligence']['count']}")
    print(f"    Asset Classes: {gui_feed['asset_class_intelligence']['count']}")

    # Verify GUI feed structure
    assert "meta" in gui_feed
    assert "overview" in gui_feed
    assert "executive_summary" in gui_feed
    assert "ai_executive_summary" in gui_feed
    assert "currency_intelligence" in gui_feed
    assert "asset_class_intelligence" in gui_feed
    assert "global_regime" in gui_feed
    assert "global_risk" in gui_feed
    print("  [PASS] GUI feed structure valid")

    # Verify GUI feed data
    assert gui_feed["overview"]["regime"] == "RISK_OFF"
    assert gui_feed["currency_intelligence"]["count"] == 3
    assert gui_feed["asset_class_intelligence"]["count"] == 2
    print("  [PASS] GUI feed data valid")

    # Test Orchestrator Feeder
    print("\n[3] Testing Orchestrator Feeder...")
    orch_feeder = OrchestratorFeeder()
    orch_feed = orch_feeder.prepare_feed(state)

    print("  Orchestrator Feed prepared:")
    print(f"    Global Context: {orch_feed['global_context']['regime']}")
    print(f"    Currencies: {orch_feed['currency_context']['count']}")
    print(f"    Asset Classes: {orch_feed['asset_class_context']['count']}")

    # Verify orchestrator feed structure
    assert "meta" in orch_feed
    assert "global_context" in orch_feed
    assert "currency_context" in orch_feed
    assert "asset_class_context" in orch_feed
    assert "decision_context" in orch_feed
    print("  [PASS] Orchestrator feed structure valid")

    # Verify orchestrator feed data
    assert orch_feed["global_context"]["regime"] == "RISK_OFF"
    assert orch_feed["currency_context"]["count"] == 3
    assert orch_feed["asset_class_context"]["count"] == 2
    assert "regime_signal" in orch_feed["decision_context"]
    assert "currency_bias" in orch_feed["decision_context"]
    assert "asset_class_bias" in orch_feed["decision_context"]
    print("  [PASS] Orchestrator feed data valid")

    # Step 4: Verify separation
    print("\n[4] Verifying Feed Separation...")

    # GUI feed has presentation fields
    gui_keys = set(gui_feed.keys())
    print(f"  GUI feed keys: {sorted(gui_keys)}")

    # Orchestrator feed has decision fields
    orch_keys = set(orch_feed.keys())
    print(f"  Orchestrator feed keys: {sorted(orch_keys)}")

    # They should be different
    assert "overview" in gui_keys
    assert "executive_summary" in gui_keys
    assert "ai_executive_summary" in gui_keys

    assert "global_context" in orch_keys
    assert "decision_context" in orch_keys

    print("  [PASS] Feeds are properly separated")
    print("     GUI feed: Presentation/display data")
    print("     Orchestrator feed: Decision context data")

    # Final summary
    print("\n" + "=" * 70)
    print("PHASE 7.7 & 7.8 TEST RESULTS")
    print("=" * 70)

    print(f"\n  GUI Feed: {len(gui_feed)} sections")
    print(f"  Orchestrator Feed: {len(orch_feed)} sections")
    print(f"\n  GUI Feed Sections: {', '.join(gui_feed.keys())}")
    print(f"  Orchestrator Sections: {', '.join(orch_feed.keys())}")

    print("\n" + "=" * 70)
    print("[PASS] PHASE 7.7 & 7.8: GUI & ORCHESTRATOR FEEDERS PASSED")
    print("=" * 70)
    print("\n" + "=" * 70)
    print("GLOBAL INTELLIGENCE BACKEND: COMPLETE")
    print("=" * 70)

    return True


if __name__ == "__main__":
    test_feeders()
