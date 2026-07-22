# -*- coding: utf-8 -*-
"""
Confluence Engine - Phase 3 Adversarial/Conflict Testing

Tests the Harmonization Core under disagreement scenarios:
- Unanimous bearish
- Moderate disagreement
- Strong contradiction
- Mixed with neutral
- Dependent evidence
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from intelligence.confluence.schemas import NormalizedSignal, Direction, SignalType
from intelligence.confluence.evidence import EvidenceCollector
from intelligence.confluence.harmonization import (
    WeightedConsensus,
    ConfluenceScore,
    ConflictDetector,
    EvidenceDeduplicator,
)


def create_signal(engine_id, score, direction, confidence=85.0, reliability=0.85):
    """Helper to create test signals."""
    return NormalizedSignal(
        engine_id=engine_id,
        domain="TEST",
        entity="USD",
        signal_type=SignalType.CURRENCY_BIAS,
        score=score,
        direction=direction,
        confidence=confidence,
        reliability=reliability,
        freshness=0.9,
        evidence_quality=0.85,
        drivers=["TEST"],
        timestamp=datetime.utcnow() - timedelta(minutes=5),
    )


def run_test(
    name,
    signals,
    expected_direction,
    expected_conflict_level,
    expected_penalty_min=0.0,
    expected_penalty_max=0.5,
    expected_confidence_min=0,
):
    """Run a single test case."""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")

    # Collect evidence
    collector = EvidenceCollector()
    for signal in signals:
        collector.add_signal(signal)

    group = collector.get_group("USD", "CURRENCY_BIAS")
    print(f"  Signals: {len(signals)}")
    for s in signals:
        print(f"    {s.engine_id}: {s.score:+.1f} {s.direction.value}")

    # Weighted Consensus
    wc = WeightedConsensus()
    consensus = wc.calculate_consensus(group)
    print(f"\n  Consensus Score: {consensus['score']:.1f}")
    print(f"  Direction: {consensus['direction']}")
    print(f"  Confidence: {consensus['confidence']:.1f}%")
    print(f"  Agreement Ratio: {consensus['agreement_ratio']:.2f}")

    # Confluence Score
    cs = ConfluenceScore()
    score = cs.calculate_score(group, consensus)
    print(f"\n  Final Score: {score['score']:.1f}")
    print(f"  Direction: {score['direction']}")
    print(f"  Confidence: {score['confidence']:.1f}%")
    print(f"  Conflict Penalty: {score['conflict_penalty']:.3f}")
    print(f"  Conflict Level: {score['conflict_level']}")

    # Conflict Detector
    cd = ConflictDetector()
    conflict_result = cd.detect_conflicts([group])
    summary = conflict_result.get("summary", {})
    print(f"\n  Conflict Distribution: {summary.get('conflict_distribution', {})}")

    # Assertions
    passed = True

    # Check direction
    if score["direction"] != expected_direction:
        print(
            f"  [FAIL] Direction: Expected {expected_direction}, got {score['direction']}"
        )
        passed = False
    else:
        print(f"  [PASS] Direction: {score['direction']}")

    # Check conflict level
    if score["conflict_level"] != expected_conflict_level:
        print(
            f"  [FAIL] Conflict Level: Expected {expected_conflict_level}, got {score['conflict_level']}"
        )
        passed = False
    else:
        print(f"  [PASS] Conflict Level: {score['conflict_level']}")

    # Check penalty range
    if not (expected_penalty_min <= score["conflict_penalty"] <= expected_penalty_max):
        print(
            f"  [FAIL] Conflict Penalty: Expected between {expected_penalty_min:.3f} and {expected_penalty_max:.3f}, got {score['conflict_penalty']:.3f}"
        )
        passed = False
    else:
        print(f"  [PASS] Conflict Penalty: {score['conflict_penalty']:.3f}")

    # Check confidence
    if score["confidence"] < expected_confidence_min:
        print(
            f"  [FAIL] Confidence: Expected > {expected_confidence_min}%, got {score['confidence']:.1f}%"
        )
        passed = False
    else:
        print(f"  [PASS] Confidence: {score['confidence']:.1f}%")

    result = "[PASS]" if passed else "[FAIL]"
    print(f"\n  RESULT: {result}")

    return passed


def test_deduplicator():
    """Test evidence deduplication with dependent signals."""
    print(f"\n{'='*70}")
    print("TEST: Evidence Deduplicator - Dependent Evidence")
    print(f"{'='*70}")

    # Create signals from dependent engines
    signals = [
        create_signal("GLB-001", 80.0, Direction.BULLISH),
        create_signal("GLB-003", 75.0, Direction.BULLISH),
        create_signal("GLB-006", 82.0, Direction.BULLISH),
    ]

    print(f"  Original signals: {len(signals)}")
    for s in signals:
        print(f"    {s.engine_id}: {s.score:+.1f}")

    # Deduplicate
    dedup = EvidenceDeduplicator()
    dedup.set_dependencies(
        {
            "GLB-003": {"GLB-001"},  # GLB-003 depends on GLB-001
            "GLB-006": {"GLB-003"},  # GLB-006 depends on GLB-003
        }
    )
    independent = dedup.deduplicate(signals)

    print(f"\n  Independent signals: {len(independent)}")
    for s in independent:
        print(f"    {s.engine_id}: {s.score:+.1f}")

    kept = [s.engine_id for s in independent]

    if "GLB-001" in kept and "GLB-003" not in kept and "GLB-006" not in kept:
        print("\n  [PASS] Deduplication correct: Only GLB-001 kept")
        return True
    else:
        print(f"\n  [FAIL] Deduplication incorrect: Kept {kept}")
        return False


def run_adversarial_tests():
    """Run all adversarial tests."""

    print("=" * 70)
    print("CONFLUENCE ENGINE - PHASE 3 ADVERSARIAL TEST SUITE")
    print("=" * 70)

    results = []

    # Test 1: Unanimous Bearish -> NONE, penalty = 0
    results.append(
        run_test(
            name="Unanimous Bearish",
            signals=[
                create_signal("GLB-001", -80.0, Direction.BEARISH),
                create_signal("GLB-003", -85.0, Direction.BEARISH),
                create_signal("GLB-006", -82.0, Direction.BEARISH),
            ],
            expected_direction="BEARISH",
            expected_conflict_level="NONE",
            expected_penalty_min=0.0,
            expected_penalty_max=0.0,
            expected_confidence_min=85,
        )
    )

    # Test 2: Moderate Disagreement -> MEDIUM, penalty 0.15-0.40
    results.append(
        run_test(
            name="Moderate Disagreement",
            signals=[
                create_signal("GLB-001", 80.0, Direction.BULLISH),
                create_signal("GLB-003", 75.0, Direction.BULLISH),
                create_signal("GLB-008", -60.0, Direction.BEARISH),
            ],
            expected_direction="BULLISH",
            expected_conflict_level="MEDIUM",
            expected_penalty_min=0.15,
            expected_penalty_max=0.40,
            expected_confidence_min=50,
        )
    )

    # Test 3: Strong Contradiction -> HIGH, penalty 0.40-0.50
    results.append(
        run_test(
            name="Strong Contradiction",
            signals=[
                create_signal("GLB-001", 90.0, Direction.BULLISH),
                create_signal("GLB-003", -90.0, Direction.BEARISH),
            ],
            expected_direction="NEUTRAL",
            expected_conflict_level="HIGH",
            expected_penalty_min=0.40,
            expected_penalty_max=0.50,
            expected_confidence_min=40,
        )
    )

    # Test 4: Mixed with Neutral -> MEDIUM, penalty 0.20-0.40
    results.append(
        run_test(
            name="Mixed with Neutral",
            signals=[
                create_signal("GLB-001", 80.0, Direction.BULLISH),
                create_signal("GLB-003", 0.0, Direction.NEUTRAL),
                create_signal("GLB-006", -40.0, Direction.BEARISH),
            ],
            expected_direction="NEUTRAL",
            expected_conflict_level="MEDIUM",
            expected_penalty_min=0.20,
            expected_penalty_max=0.40,
            expected_confidence_min=40,
        )
    )

    # Test 5: Deduplicator
    results.append(test_deduplicator())

    # Summary
    print("\n" + "=" * 70)
    print("ADVERSARIAL TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results if r)
    total = len(results)

    print(f"\n  [PASS] Passed: {passed}")
    print(f"  [FAIL] Failed: {total - passed}")
    print(f"  Total: {total}")

    if passed == total:
        print("\n" + "=" * 70)
        print("[RESULT] Phase 3 Adversarial Tests: ALL PASSED")
        print("=" * 70)
        print("\n" + "=" * 70)
        print("PHASE 3 HARMONIZATION CORE: CERTIFIED")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print(f"[RESULT] Phase 3 Adversarial Tests: {passed}/{total} PASSED")
        print("=" * 70)

    return passed == total


if __name__ == "__main__":
    run_adversarial_tests()
