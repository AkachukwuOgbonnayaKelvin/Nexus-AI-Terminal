"""
Phase 7: Global Intelligence Hub - Integration Test
"""

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from intelligence.confluence.contracts import (
    AssetClass,
    AssetClassRating,
    Direction,
    EntityType,
    GlobalEntityRating,
    GlobalIntelligenceOutput,
)
from intelligence.global_hub import (
    AIExecutiveInterpreter,
    DeterministicSummaryEngine,
    IngestionGateway,
    OverviewViewModel,
    StateManager,
)


def create_test_output() -> GlobalIntelligenceOutput:
    """Create test GlobalIntelligenceOutput."""
    # Create entity ratings
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
            entity="EUR",
            entity_type=EntityType.CURRENCY,
            score=45.0,
            direction=Direction.BULLISH,
            confidence=70.0,
            rank=3,
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
            entity="GBP",
            entity_type=EntityType.CURRENCY,
            score=38.0,
            direction=Direction.BULLISH,
            confidence=65.0,
            rank=4,
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

    # Create asset-class ratings
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
            asset_class=AssetClass.ENERGY,
            name="Energy",
            score=57.0,
            direction=Direction.BULLISH,
            confidence=70.0,
            rank=2,
        ),
        AssetClassRating(
            asset_class=AssetClass.FX,
            name="FX",
            score=45.9,
            direction=Direction.BULLISH,
            confidence=75.1,
            rank=3,
        ),
        AssetClassRating(
            asset_class=AssetClass.BONDS,
            name="Bonds",
            score=41.0,
            direction=Direction.BULLISH,
            confidence=68.0,
            rank=4,
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


def test_phase7_integration():
    """Run Phase 7 integration test."""

    print("=" * 70)
    print("PHASE 7: GLOBAL INTELLIGENCE HUB - INTEGRATION TEST")
    print("=" * 70)

    # Step 1: Test Ingestion Gateway
    print("\n[1] Testing Ingestion Gateway...")
    gateway = IngestionGateway()
    output = create_test_output()
    result = gateway.ingest(output)
    print(f"  Ingestion result: {result}")

    assert result["status"] == "accepted", (
        f"Expected 'accepted', got {result['status']}"
    )
    print("  ✅ Ingestion accepted")

    # Step 2: Test State Manager
    print("\n[2] Testing State Manager...")
    manager = StateManager()
    state = manager.build_state(output)
    print(f"  State created: {state.state_id}")
    print(f"    Regime: {state.global_regime}")
    print(f"    Currencies: {len(state.currency_rankings)}")
    print(f"    Asset classes: {len(state.asset_class_rankings)}")

    assert state.global_regime == "RISK_OFF"
    assert len(state.currency_rankings) == 5
    print("  ✅ State built correctly")

    # Step 3: Test Deterministic Summary
    print("\n[3] Testing Deterministic Summary Engine...")
    summary_engine = DeterministicSummaryEngine()
    structured = summary_engine.generate_structured_summary(state)
    print("  Structured summary:")
    print(f"    Regime: {structured['regime']}")
    print(
        f"    Strongest currency: {structured.get('strongest_currency', {}).get('entity')}"
    )
    print(
        f"    Strongest asset: {structured.get('strongest_asset_class', {}).get('name')}"
    )
    print(f"    Summary: {structured['summary_text'][:80]}...")

    assert structured["regime"] == "RISK_OFF"
    assert structured["strongest_currency"]["entity"] == "USD"
    print("  ✅ Deterministic summary generated")

    # Step 4: Test AI Executive Interpreter
    print("\n[4] Testing AI Executive Interpreter...")
    interpreter = AIExecutiveInterpreter(use_llm=False)
    interpretation = interpreter.interpret(state, structured)
    print("  AI Interpretation:")
    print(f"    Narrative: {interpretation['narrative'][:60]}...")
    print(f"    Dominant theme: {interpretation['dominant_theme']}")
    print(f"    Confidence: {interpretation['confidence']}%")

    assert interpretation["dominant_theme"] == "Defensive capital rotation"
    print("  ✅ AI interpretation generated")

    # Step 5: Test Overview View Model
    print("\n[5] Testing Overview View Model...")
    view_model = OverviewViewModel.from_state(state)
    print("  Overview View Model:")
    print(f"    Regime: {view_model.regime}")
    print(f"    Risk: {view_model.risk_level}")
    print(f"    Top currencies: {len(view_model.top_currencies)}")
    print(f"    Top asset classes: {len(view_model.top_asset_classes)}")

    assert view_model.regime == "RISK_OFF"
    assert len(view_model.top_currencies) == 5
    print("  ✅ Overview view model created")

    # Step 6: Test State Manager get_current_state
    print("\n[6] Testing State Manager retrieval...")
    current = manager.get_current_state()
    print(f"  Current state ID: {current.state_id}")
    print(f"  Valid until: {current.valid_until}")

    assert current is not None
    assert current.state_id == state.state_id
    print("  ✅ State retrieval works")

    # Step 7: Test state validity
    print("\n[7] Testing state validity...")
    is_valid = manager.is_valid(state)
    print(f"  State valid: {is_valid}")

    # Create expired state
    expired_state = state
    expired_state.valid_until = datetime.utcnow() - timedelta(hours=1)
    is_expired_valid = manager.is_valid(expired_state)
    print(f"  Expired state valid: {is_expired_valid}")

    assert is_valid is True
    assert is_expired_valid is False
    print("  ✅ State validity checks work")

    # Final summary
    print("\n" + "=" * 70)
    print("PHASE 7 TEST RESULTS")
    print("=" * 70)

    print(f"\n  State ID: {state.state_id}")
    print(f"  Regime: {state.global_regime}")
    print(f"  Currencies: {len(state.currency_rankings)}")
    print(f"  Asset Classes: {len(state.asset_class_rankings)}")

    print("\n" + "=" * 70)
    print("✅ PHASE 7: GLOBAL INTELLIGENCE HUB PASSED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    test_phase7_integration()
