"""
Phase 6: Distribution API - Integration Test

Tests the complete Phase 6 pipeline:
1. Package Assembly
2. Output Validation
3. Global Output Builder
4. Asset Feed Builder
5. Envelope Creation
6. Routing
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from intelligence.confluence.contracts import (
    ConflictLevel,
    Direction,
    EntityType,
    GlobalEntityRating,
    GlobalRisk,
    HarmonizedResult,
)
from intelligence.confluence.distribution import (
    AssetFeedBuilder,
    DistributionRouter,
    EnvelopeFactory,
    GlobalOutputBuilder,
    OutputAssembler,
    OutputStatus,
    OutputType,
    OutputValidator,
)


def create_test_entity_ratings() -> list:
    """Create test entity ratings (simulating Phase 4 output)."""
    return [
        GlobalEntityRating(
            entity="USD",
            entity_type=EntityType.CURRENCY,
            score=84.0,
            direction=Direction.BULLISH,
            confidence=86.5,
            supporting_engines=["GLB-001", "GLB-003", "GLB-005"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="EUR",
            entity_type=EntityType.CURRENCY,
            score=45.0,
            direction=Direction.BULLISH,
            confidence=70.0,
            supporting_engines=["GLB-001", "GLB-003"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="JPY",
            entity_type=EntityType.CURRENCY,
            score=74.0,
            direction=Direction.BULLISH,
            confidence=82.0,
            supporting_engines=["GLB-001", "GLB-006", "GLB-007"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="GBP",
            entity_type=EntityType.CURRENCY,
            score=38.0,
            direction=Direction.BULLISH,
            confidence=65.0,
            supporting_engines=["GLB-003"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="AUD",
            entity_type=EntityType.CURRENCY,
            score=-24.0,
            direction=Direction.BEARISH,
            confidence=72.0,
            supporting_engines=["GLB-008"],
            contradicting_engines=["GLB-001", "GLB-003"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="XAUUSD",
            entity_type=EntityType.COMMODITY,
            score=81.0,
            direction=Direction.BULLISH,
            confidence=84.0,
            supporting_engines=["GLB-001", "GLB-006", "GLB-007"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="US500",
            entity_type=EntityType.INDEX,
            score=-63.0,
            direction=Direction.BEARISH,
            confidence=78.0,
            supporting_engines=["GLB-008"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="US10Y",
            entity_type=EntityType.BOND,
            score=41.0,
            direction=Direction.BULLISH,
            confidence=68.0,
            supporting_engines=["GLB-003"],
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="CL=F",
            entity_type=EntityType.COMMODITY,
            score=57.0,
            direction=Direction.BULLISH,
            confidence=70.0,
            supporting_engines=["GLB-007"],
            drivers=[],
            risks=[],
        ),
    ]


def create_test_asset_class_ratings() -> list:
    """Create test asset-class ratings (simulating Phase 5 output)."""
    from intelligence.confluence.asset_class.rating_engine import AssetClassRatingEngine

    # Build from entity ratings
    entity_ratings = create_test_entity_ratings()
    from intelligence.confluence.asset_class.aggregator import AssetClassAggregator

    aggregator = AssetClassAggregator()
    grouped = aggregator.aggregate(entity_ratings)

    engine = AssetClassRatingEngine()
    return engine.rate_asset_classes(grouped)


def create_test_harmonized_results() -> list:
    """Create test harmonized results (simulating Phase 3 output)."""
    return [
        HarmonizedResult(
            entity="USD",
            entity_type="CURRENCY",
            consensus_score=84.0,
            final_score=84.0,
            direction=Direction.BULLISH,
            confidence=86.5,
            agreement_ratio=0.9,
            conflict_level=ConflictLevel.NONE,
            conflict_penalty=0.0,
            evidence_count=3,
            supporting_engines=["GLB-001", "GLB-003", "GLB-005"],
        ),
        HarmonizedResult(
            entity="AUD",
            entity_type="CURRENCY",
            consensus_score=-24.0,
            final_score=-24.0,
            direction=Direction.BEARISH,
            confidence=72.0,
            agreement_ratio=0.7,
            conflict_level=ConflictLevel.MEDIUM,
            conflict_penalty=0.15,
            evidence_count=3,
            supporting_engines=["GLB-008"],
            contradicting_engines=["GLB-001", "GLB-003"],
        ),
    ]


def test_phase6_distribution():
    """Run Phase 6 integration test."""

    print("=" * 70)
    print("PHASE 6: DISTRIBUTION API - INTEGRATION TEST")
    print("=" * 70)

    # Step 1: Create test data
    print("\n[1] Creating Test Data...")
    entity_ratings = create_test_entity_ratings()
    asset_class_ratings = create_test_asset_class_ratings()
    harmonized_results = create_test_harmonized_results()

    print(f"  Entity ratings: {len(entity_ratings)}")
    print(f"  Asset-class ratings: {len(asset_class_ratings)}")
    print(f"  Harmonized results: {len(harmonized_results)}")

    # Step 2: Test Output Assembler
    print("\n[2] Testing Output Assembler...")
    assembler = OutputAssembler()
    package = assembler.assemble(
        entity_ratings=entity_ratings,
        asset_class_ratings=asset_class_ratings,
        harmonized_results=harmonized_results,
        global_regime="RISK_OFF",
        global_regime_confidence=84.0,
        global_risk_level="MEDIUM",
        global_risk_score=45.0,
        key_drivers=["RISK_OFF", "SAFE_HAVEN", "USD_STRENGTH"],
        global_risks=[
            GlobalRisk(
                name="EQUITY_DOWNSIDE",
                severity=65.0,
                description="Equity downside risk",
            ),
            GlobalRisk(
                name="GEOPOLITICAL", severity=55.0, description="Geopolitical risk"
            ),
        ],
    )
    print(f"  Package created: {package}")

    # Step 3: Test Output Validator
    print("\n[3] Testing Output Validator...")
    validator = OutputValidator()

    # Validate entity ratings
    entity_result = validator.validate_entity_ratings(entity_ratings)
    print(f"  Entity validation: {entity_result}")

    # Validate asset-class ratings
    class_result = validator.validate_asset_class_ratings(asset_class_ratings)
    print(f"  Asset-class validation: {class_result}")

    # Step 4: Test Global Output Builder
    print("\n[4] Testing Global Output Builder...")
    builder = GlobalOutputBuilder()
    global_output = builder.build(package)
    print("  Global output built:")
    print(f"    Regime: {global_output.global_regime}")
    print(f"    Currencies: {len(global_output.currency_rankings)}")
    print(f"    Asset classes: {len(global_output.asset_class_rankings)}")
    print(f"    Executive summary: {global_output.executive_summary[:50]}...")

    # Step 5: Test Asset Feed Builder
    print("\n[5] Testing Asset Feed Builder...")
    feed_builder = AssetFeedBuilder()

    # Test for specific entity
    audusd_feed = feed_builder.build_for_entity("AUDUSD", package)
    if audusd_feed:
        print("  AUDUSD feed built:")
        print(f"    Symbol: {audusd_feed.symbol}")
        print(f"    Global bias: {audusd_feed.global_bias.value}")
        print(f"    Global score: {audusd_feed.global_score:+.1f}")
        print(f"    Status: {audusd_feed.status.value}")

    # Build all feeds
    all_feeds = feed_builder.build_for_all_entities(package)
    print(f"  All feeds built: {len(all_feeds)}")

    # Step 6: Test Envelope Factory
    print("\n[6] Testing Envelope Factory...")
    global_envelope = EnvelopeFactory.create_global_envelope(global_output)
    print(f"  Global envelope: {global_envelope}")
    print(f"    Status: {global_envelope.status.value}")
    print(f"    Valid: {global_envelope.is_valid()}")

    feed_envelopes = EnvelopeFactory.create_asset_feeds_envelope(all_feeds)
    print(f"  Feed envelopes: {len(feed_envelopes)}")

    # Step 7: Test Distribution Router
    print("\n[7] Testing Distribution Router...")
    router = DistributionRouter()
    result = router.route(package)

    print("  Routing result:")
    print(f"    Status: {result.get('status', 'error')}")
    if "global_output" in result:
        print(f"    Global output: {result['global_output']}")
    if "asset_feeds" in result:
        print(f"    Asset feeds: {len(result['asset_feeds'])}")
    if "health" in result:
        health = result["health"]
        print(f"    Health: {'✅ Healthy' if health['healthy'] else '⚠️ Issues'}")
        if health.get("errors"):
            print(f"    Errors: {health['errors']}")

    # Step 8: Validate Results
    print("\n[8] Validating Results...")

    # Check global output
    assert global_output.global_regime == "RISK_OFF"
    assert len(global_output.currency_rankings) == 5
    assert len(global_output.asset_class_rankings) == 5
    print("  ✅ Global output valid")

    # Check asset feeds
    assert len(all_feeds) > 0
    print(f"  ✅ {len(all_feeds)} asset feeds generated")

    # Check envelopes
    assert global_envelope.status == OutputStatus.FINAL
    assert global_envelope.output_type == OutputType.GLOBAL_INTELLIGENCE
    print("  ✅ Envelope status correct")

    # Check router result
    assert result.get("status") == "success"
    print("  ✅ Router execution successful")

    # Final summary
    print("\n" + "=" * 70)
    print("PHASE 6 TEST RESULTS")
    print("=" * 70)

    print(f"\n  Package: {package}")
    print(f"  Global Output: {global_output}")
    print(f"  Asset Feeds: {len(all_feeds)}")
    print(f"  Envelopes: {len(feed_envelopes) + 1}")
    print(f"  Health: {'✅ Healthy' if result['health']['healthy'] else '⚠️ Issues'}")

    print("\n" + "=" * 70)
    print("✅ PHASE 6: DISTRIBUTION API & OUTPUT CONTRACTS PASSED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    test_phase6_distribution()
