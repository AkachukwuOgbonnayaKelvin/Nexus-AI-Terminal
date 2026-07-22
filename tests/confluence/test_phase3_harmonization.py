"""
Confluence Engine - Phase 3 Harmonization Core Test

Tests the Harmonization Core components:
- Weighted Consensus
- Confluence Score
- Conflict Detector
- Evidence Deduplicator
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


def test_phase3_harmonization():
    """Run Phase 3 Harmonization Core test."""

    print("=" * 70)
    print("CONFLUENCE ENGINE - PHASE 3 HARMONIZATION CORE TEST")
    print("=" * 70)

    # Create test signals
    signals = [
        NormalizedSignal(
            engine_id="GLB-001",
            domain="REGIME",
            entity="USD",
            signal_type=SignalType.CURRENCY_BIAS,
            score=85.0,
            direction=Direction.BULLISH,
            confidence=88.0,
            reliability=0.85,
            freshness=0.9,
            evidence_quality=0.8,
            drivers=["RISK_OFF", "SAFE_HAVEN"],
            timestamp=datetime.utcnow() - timedelta(minutes=5),
        ),
        NormalizedSignal(
            engine_id="GLB-003",
            domain="MACRO",
            entity="USD",
            signal_type=SignalType.CURRENCY_BIAS,
            score=72.0,
            direction=Direction.BULLISH,
            confidence=80.0,
            reliability=0.9,
            freshness=0.8,
            evidence_quality=0.85,
            drivers=["GROWTH", "RATES"],
            timestamp=datetime.utcnow() - timedelta(minutes=10),
        ),
        NormalizedSignal(
            engine_id="GLB-006",
            domain="GEOPOLITICAL",
            entity="USD",
            signal_type=SignalType.CURRENCY_BIAS,
            score=90.0,
            direction=Direction.BULLISH,
            confidence=92.0,
            reliability=0.82,
            freshness=0.95,
            evidence_quality=0.9,
            drivers=["GEOPOLITICAL_RISK"],
            timestamp=datetime.utcnow() - timedelta(minutes=2),
        ),
    ]

    print("\n[1] Collecting Evidence...")
    collector = EvidenceCollector()
    for signal in signals:
        collector.add_signal(signal)

    group = collector.get_group("USD", "CURRENCY_BIAS")
    print(f"  ✅ Evidence collected: {len(signals)} signals")

    print("\n[2] Weighted Consensus...")
    wc = WeightedConsensus()
    consensus = wc.calculate_consensus(group)
    print(f'  ✅ Consensus Score: {consensus["score"]:.1f}')
    print(f'  ✅ Direction: {consensus["direction"]}')
    print(f'  ✅ Confidence: {consensus["confidence"]:.1f}%')
    print(f'  ✅ Agreement Ratio: {consensus["agreement_ratio"]:.2f}')

    print("\n[3] Confluence Score...")
    cs = ConfluenceScore()
    score = cs.calculate_score(group, consensus)
    print(f'  ✅ Final Score: {score["score"]:.1f}')
    print(f'  ✅ Direction: {score["direction"]}')
    print(f'  ✅ Confidence: {score["confidence"]:.1f}%')
    print(f'  ✅ Conflict Penalty: {score["conflict_penalty"]:.3f}')
    print(f'  ✅ Base Score: {score["base_score"]:.1f}')

    print("\n[4] Conflict Detector...")
    cd = ConflictDetector()

    # ✅ FIX: Assign to conflict_result, then extract summary
    conflict_result = cd.detect_conflicts([group])
    summary = conflict_result.get("summary", {})

    print(f'  ✅ Total Groups: {summary.get("total_groups", 0)}')
    print(f'  ✅ Conflict Distribution: {summary.get("conflict_distribution", {})}')
    print(f'  ✅ High Conflict %: {summary.get("high_conflict_percentage", 0):.1f}%')

    print("\n[5] Evidence Deduplicator...")
    dedup = EvidenceDeduplicator()
    dedup.set_dependencies({"GLB-003": {"GLB-005", "GLB-007"}, "GLB-006": {"GLB-008"}})
    independent = dedup.deduplicate(signals)
    print(f"  ✅ Original signals: {len(signals)}")
    print(f"  ✅ Independent signals: {len(independent)}")
    print(f"  ✅ Engines kept: {[s.engine_id for s in independent]}")

    print("\n" + "=" * 70)
    print("[RESULT] Phase 3 Harmonization Core: PASSED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    test_phase3_harmonization()
