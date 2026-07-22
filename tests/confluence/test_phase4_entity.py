# -*- coding: utf-8 -*-
"""
Phase 4: Global Entity Intelligence - Integration Test

Tests the complete Phase 4 pipeline:
1. Entity Classification
2. Entity Aggregation
3. Entity Rating
4. Entity Ranking
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from intelligence.confluence.contracts import HarmonizedResult, Direction, ConflictLevel
from intelligence.confluence.entity import (
    EntityClassifier,
    EntityAggregator,
    EntityRatingEngine,
    EntityRanker,
)


def create_test_result(
    entity: str,
    score: float,
    direction: Direction,
    confidence: float,
    supporting=None,
    contradicting=None,
    drivers=None,
    risks=None,
) -> HarmonizedResult:
    """Create a test HarmonizedResult."""
    return HarmonizedResult(
        entity=entity,
        entity_type=EntityClassifier.classify(entity),
        consensus_score=score,
        final_score=score,
        direction=direction,
        confidence=confidence,
        agreement_ratio=0.85,
        conflict_level=ConflictLevel.NONE,
        conflict_penalty=0.0,
        evidence_count=3,
        supporting_engines=supporting or [],
        contradicting_engines=contradicting or [],
        drivers=drivers or [],
        risks=risks or [],
    )


def test_phase4_entity_intelligence():
    """Run Phase 4 integration test."""

    print("=" * 70)
    print("PHASE 4: GLOBAL ENTITY INTELLIGENCE - INTEGRATION TEST")
    print("=" * 70)

    # Step 1: Create test harmonized results
    print("\n[1] Creating Harmonized Results...")

    results = [
        create_test_result(
            "USD",
            86.0,
            Direction.BULLISH,
            88.0,
            supporting=["GLB-001", "GLB-003", "GLB-005"],
            drivers=["CENTRAL_BANK_SUPPORT", "SAFE_HAVEN_FLOW"],
            risks=["SENTIMENT_DIVERGENCE"],
        ),
        create_test_result(
            "USD",
            82.0,
            Direction.BULLISH,
            85.0,
            supporting=["GLB-006", "GLB-007"],
            drivers=["CAPITAL_INFLOW"],
            risks=["POSITIONING_CROWDED"],
        ),
        create_test_result(
            "EUR",
            45.0,
            Direction.BULLISH,
            70.0,
            supporting=["GLB-001", "GLB-003"],
            drivers=["MACRO_STABILITY"],
            risks=["POLITICAL_RISK"],
        ),
        create_test_result(
            "JPY",
            74.0,
            Direction.BULLISH,
            82.0,
            supporting=["GLB-001", "GLB-006", "GLB-007"],
            drivers=["SAFE_HAVEN_FLOW"],
            risks=["INTERVENTION_RISK"],
        ),
        create_test_result(
            "GBP",
            38.0,
            Direction.NEUTRAL,
            65.0,
            supporting=["GLB-003"],
            drivers=["ECONOMIC_RECOVERY"],
            risks=["BREXIT_UNCERTAINTY"],
        ),
        create_test_result(
            "AUD",
            -24.0,
            Direction.BEARISH,
            72.0,
            supporting=["GLB-008"],
            contradicting=["GLB-001", "GLB-003"],
            drivers=["COMMODITY_WEAKNESS"],
            risks=["CHINA_SLOWDOWN"],
        ),
        create_test_result(
            "XAUUSD",
            81.0,
            Direction.BULLISH,
            84.0,
            supporting=["GLB-001", "GLB-006", "GLB-007"],
            drivers=["REAL_YIELD_DECLINE", "SAFE_HAVEN_DEMAND"],
            risks=["DOLLAR_STRENGTH"],
        ),
    ]

    print(f"  Created {len(results)} harmonized results")
    for r in results:
        print(f"    {r.entity}: {r.final_score:+.1f} {r.direction.value}")

    # Step 2: Test Entity Classifier
    print("\n[2] Testing Entity Classifier...")
    for entity in ["USD", "EUR", "XAUUSD", "CL=F", "US10Y", "US500"]:
        entity_type = EntityClassifier.classify(entity)
        print(f"    {entity} -> {entity_type.value}")

    # Step 3: Test Entity Aggregator
    print("\n[3] Testing Entity Aggregator...")
    aggregator = EntityAggregator()
    grouped = aggregator.aggregate(results)
    print(f"  Grouped into {len(grouped)} entities:")
    for entity, items in grouped.items():
        print(f"    {entity}: {len(items)} results")

    # Step 4: Test Entity Rating Engine
    print("\n[4] Testing Entity Rating Engine...")
    engine = EntityRatingEngine()
    ratings = engine.rate_entities(grouped)
    print(f"  Generated {len(ratings)} entity ratings:")
    for r in ratings:
        print(
            f"    {r.entity}: {r.score:+.1f} {r.direction.value} (conf: {r.confidence:.1f}%)"
        )

    # Step 5: Test Entity Ranker
    print("\n[5] Testing Entity Ranker...")
    ranker = EntityRanker()
    ranked = ranker.rank_entities(ratings)
    print("  Global Rankings:")
    for r in ranked:
        print(f"    #{r.rank}: {r.entity} {r.score:+.1f} {r.direction.value}")

    # Step 6: Test Currency Rankings
    print("\n[6] Testing Currency Rankings...")
    currency_rankings = ranker.rank_currencies(ratings)
    print("  Currency Rankings:")
    for r in currency_rankings:
        print(f"    #{r.rank}: {r.entity} {r.score:+.1f} {r.direction.value}")

    # Step 7: Validate results
    print("\n[7] Validating Results...")

    # Check USD has highest score
    strongest = ranker.get_strongest_currency(ratings)
    if strongest and strongest.entity == "USD":
        print(f"  ✅ Strongest currency: {strongest.entity} ({strongest.score:+.1f})")
    else:
        print(
            f"  ❌ Expected USD as strongest, got {strongest.entity if strongest else 'None'}"
        )
        return False

    # Check AUD is weakest
    weakest = ranker.get_weakest_currency(ratings)
    if weakest and weakest.entity == "AUD":
        print(f"  ✅ Weakest currency: {weakest.entity} ({weakest.score:+.1f})")
    else:
        print(
            f"  ❌ Expected AUD as weakest, got {weakest.entity if weakest else 'None'}"
        )
        return False

    # Check XAUUSD is rated correctly
    xau_ratings = [r for r in ratings if r.entity == "XAUUSD"]
    if xau_ratings and xau_ratings[0].direction == Direction.BULLISH:
        print(
            f"  ✅ XAUUSD rated: {xau_ratings[0].score:+.1f} {xau_ratings[0].direction.value}"
        )
    else:
        print("  ❌ XAUUSD rating incorrect")
        return False

    # Check ranking order
    print("\n[8] Checking Ranking Order...")
    expected_order = ["USD", "XAUUSD", "JPY", "EUR", "GBP", "AUD"]
    actual_order = [r.entity for r in ranked]

    if actual_order == expected_order:
        print(f"  ✅ Ranking order correct: {actual_order}")
    else:
        print("  ❌ Ranking order incorrect")
        print(f"     Expected: {expected_order}")
        print(f"     Actual:   {actual_order}")
        return False

    # Final summary
    print("\n" + "=" * 70)
    print("PHASE 4 TEST RESULTS")
    print("=" * 70)

    print(f"\n  Entities Processed: {len(ratings)}")
    print(f"  Currencies Ranked: {len(currency_rankings)}")
    print("\n  Top 3 Entities:")
    for r in ranked[:3]:
        print(f"    #{r.rank}: {r.entity} {r.score:+.1f} {r.direction.value}")

    print("\n  Top 3 Currencies:")
    for r in currency_rankings[:3]:
        print(f"    #{r.rank}: {r.entity} {r.score:+.1f} {r.direction.value}")

    print("\n" + "=" * 70)
    print("✅ PHASE 4: GLOBAL ENTITY INTELLIGENCE PASSED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    test_phase4_entity_intelligence()
