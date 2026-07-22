# -*- coding: utf-8 -*-
"""
Phase 5: Asset-Class Intelligence - Integration Test

Tests the complete Phase 5 pipeline:
1. Asset-Class Mapping
2. Asset-Class Aggregation
3. Asset-Class Rating
4. Asset-Class Ranking
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from intelligence.confluence.contracts import (
    GlobalEntityRating,
    AssetClass,
    EntityType,
    Direction,
)
from intelligence.confluence.asset_class import (
    AssetClassMapper,
    AssetClassAggregator,
    AssetClassRatingEngine,
    AssetClassRanker,
)


def create_test_entity_ratings() -> list:
    """Create test entity ratings."""

    # Simulate Phase 4 output
    return [
        GlobalEntityRating(
            entity="USD",
            entity_type=EntityType.CURRENCY,
            score=84.0,
            direction=Direction.BULLISH,
            confidence=86.5,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="EUR",
            entity_type=EntityType.CURRENCY,
            score=45.0,
            direction=Direction.BULLISH,
            confidence=70.0,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="JPY",
            entity_type=EntityType.CURRENCY,
            score=74.0,
            direction=Direction.BULLISH,
            confidence=82.0,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="GBP",
            entity_type=EntityType.CURRENCY,
            score=38.0,
            direction=Direction.BULLISH,
            confidence=65.0,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="AUD",
            entity_type=EntityType.CURRENCY,
            score=-24.0,
            direction=Direction.BEARISH,
            confidence=72.0,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="XAUUSD",
            entity_type=EntityType.COMMODITY,
            score=81.0,
            direction=Direction.BULLISH,
            confidence=84.0,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="US500",
            entity_type=EntityType.INDEX,
            score=-63.0,
            direction=Direction.BEARISH,
            confidence=78.0,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="US10Y",
            entity_type=EntityType.BOND,
            score=41.0,
            direction=Direction.BULLISH,
            confidence=68.0,
            drivers=[],
            risks=[],
        ),
        GlobalEntityRating(
            entity="CL=F",
            entity_type=EntityType.COMMODITY,
            score=57.0,
            direction=Direction.BULLISH,
            confidence=70.0,
            drivers=[],
            risks=[],
        ),
    ]


def test_phase5_asset_class():
    """Run Phase 5 integration test."""

    print("=" * 70)
    print("PHASE 5: ASSET-CLASS INTELLIGENCE - INTEGRATION TEST")
    print("=" * 70)

    # Step 1: Create entity ratings
    print("\n[1] Creating Entity Ratings...")
    ratings = create_test_entity_ratings()
    print(f"  Created {len(ratings)} entity ratings:")
    for r in ratings:
        print(f"    {r.entity}: {r.score:+.1f} {r.direction.value}")

    # Step 2: Test Asset-Class Mapper
    print("\n[2] Testing Asset-Class Mapper...")
    mapper = AssetClassMapper()

    test_entities = ["USD", "EUR", "XAUUSD", "US500", "US10Y", "CL=F"]
    for entity in test_entities:
        asset_class = mapper.map_entity(entity)
        print(f"    {entity} -> {asset_class.value if asset_class else 'UNKNOWN'}")

    # Step 3: Test Asset-Class Aggregator
    print("\n[3] Testing Asset-Class Aggregator...")
    aggregator = AssetClassAggregator()
    grouped = aggregator.aggregate(ratings)
    print(f"  Grouped into {len(grouped)} asset classes:")
    for asset_class, items in grouped.items():
        entities = [r.entity for r in items]
        print(f"    {asset_class.value}: {len(items)} entities: {entities}")

    # Step 4: Test Asset-Class Rating Engine
    print("\n[4] Testing Asset-Class Rating Engine...")
    engine = AssetClassRatingEngine()
    class_ratings = engine.rate_asset_classes(grouped)
    print(f"  Generated {len(class_ratings)} asset-class ratings:")
    for r in class_ratings:
        print(
            f"    {r.name}: {r.score:+.1f} {r.direction.value} (conf: {r.confidence:.1f}%)"
        )

    # Step 5: Test Asset-Class Ranker
    print("\n[5] Testing Asset-Class Ranker...")
    ranker = AssetClassRanker()
    ranked = ranker.rank_asset_classes(class_ratings)
    print("  Asset-Class Rankings (by score descending):")
    for r in ranked:
        print(f"    #{r.rank}: {r.name} {r.score:+.1f} {r.direction.value}")

    # Step 6: Validate Results
    print("\n[6] Validating Results...")

    # Check FX class exists
    fx_ratings = [r for r in class_ratings if r.asset_class == AssetClass.FX]
    if fx_ratings:
        print(
            f"  ✅ FX rated: {fx_ratings[0].score:+.1f} {fx_ratings[0].direction.value}"
        )
    else:
        print("  ❌ FX class not found")
        return False

    # Check Metals class exists and is strong
    metals_ratings = [r for r in class_ratings if r.asset_class == AssetClass.METALS]
    if metals_ratings and metals_ratings[0].score > 70:
        print(
            f"  ✅ Metals rated: {metals_ratings[0].score:+.1f} {metals_ratings[0].direction.value}"
        )
    else:
        print("  ❌ Metals rating too low or not found")
        return False

    # Check Equities class exists and is weak
    equities_ratings = [
        r for r in class_ratings if r.asset_class == AssetClass.EQUITIES
    ]
    if equities_ratings and equities_ratings[0].score < -50:
        print(
            f"  ✅ Equities rated: {equities_ratings[0].score:+.1f} {equities_ratings[0].direction.value}"
        )
    else:
        print("  ❌ Equities rating not bearish enough or not found")
        return False

    # Check Energy class exists
    energy_ratings = [r for r in class_ratings if r.asset_class == AssetClass.ENERGY]
    if energy_ratings:
        print(
            f"  ✅ Energy rated: {energy_ratings[0].score:+.1f} {energy_ratings[0].direction.value}"
        )
    else:
        print("  ❌ Energy class not found")
        return False

    # Step 7: Check ranking order (score descending)
    print("\n[7] Checking Ranking Order...")

    # Get scores in ranking order
    ranking_scores = [(r.name, r.score) for r in ranked]
    print(f"  Ranking scores: {ranking_scores}")

    # Verify scores are descending
    scores = [r.score for r in ranked]
    is_descending = all(scores[i] >= scores[i + 1] for i in range(len(scores) - 1))

    if is_descending:
        print(
            f"  ✅ Ranking order correct (scores descending): {[r.name for r in ranked]}"
        )
    else:
        print("  ❌ Ranking order not descending")
        return False

    # Verify rank numbers are sequential
    ranks = [r.rank for r in ranked]
    if ranks == list(range(1, len(ranks) + 1)):
        print(f"  ✅ Rank numbers sequential: {ranks}")
    else:
        print(f"  ❌ Rank numbers not sequential: {ranks}")
        return False

    # Step 8: Expected order based on actual scores
    print("\n[8] Expected Ranking (by score descending)...")
    expected_order = ["Metals", "Energy", "FX", "Bonds", "Equities"]
    actual_order = [r.name for r in ranked]

    if actual_order == expected_order:
        print(f"  ✅ Expected order correct: {expected_order}")
    else:
        print("  ❌ Expected order mismatch")
        print(f"     Expected: {expected_order}")
        print(f"     Actual:   {actual_order}")
        return False

    # Final summary
    print("\n" + "=" * 70)
    print("PHASE 5 TEST RESULTS")
    print("=" * 70)

    print(f"\n  Asset Classes Processed: {len(class_ratings)}")
    print("\n  Final Rankings (by score descending):")
    for r in ranked:
        print(f"    #{r.rank}: {r.name} {r.score:+.1f} {r.direction.value}")

    print("\n" + "=" * 70)
    print("✅ PHASE 5: ASSET-CLASS INTELLIGENCE PASSED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    test_phase5_asset_class()
