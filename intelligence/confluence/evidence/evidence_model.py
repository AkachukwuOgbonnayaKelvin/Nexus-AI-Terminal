"""
Confluence Engine - Evidence Model

Defines how evidence is collected, validated, and scored.
"""

from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from ..schemas import NormalizedSignal, Evidence, ConflictLevel, Direction, SignalType


@dataclass
class EvidenceEntry:
    """Individual evidence entry with quality scoring"""

    signal: NormalizedSignal
    quality_score: float = 0.0
    is_duplicate: bool = False
    duplicate_of: Optional[str] = None

    def calculate_quality(self) -> float:
        """Calculate overall quality score"""
        if not self.signal:
            return 0.0

        # Combine reliability, confidence, freshness, and evidence quality
        quality = (
            self.signal.reliability * 0.30
            + (self.signal.confidence / 100) * 0.30
            + self.signal.freshness * 0.20
            + self.signal.evidence_quality * 0.20
        )

        self.quality_score = min(1.0, quality)
        return self.quality_score


@dataclass
class EvidenceGroup:
    """Group of evidence for a single entity"""

    entity: str
    signal_type: str
    evidence: List[EvidenceEntry] = field(default_factory=list)

    def add_evidence(self, signal: NormalizedSignal) -> None:
        """Add evidence to the group"""
        entry = EvidenceEntry(signal=signal)
        entry.calculate_quality()
        self.evidence.append(entry)

    def get_consensus_score(self) -> float:
        """Calculate weighted consensus score"""
        if not self.evidence:
            return 0.0

        total_weight = 0.0
        weighted_sum = 0.0

        for entry in self.evidence:
            weight = entry.quality_score
            if weight > 0.3:  # Only include quality evidence
                weighted_sum += entry.signal.score * weight
                total_weight += weight

        if total_weight == 0:
            return 0.0

        return weighted_sum / total_weight

    def get_consensus_direction(self) -> str:
        """Get consensus direction"""
        score = self.get_consensus_score()
        if score > 10:
            return "BULLISH"
        elif score < -10:
            return "BEARISH"
        return "NEUTRAL"

    def get_confidence(self) -> float:
        """Calculate confidence from evidence"""
        if not self.evidence:
            return 0.0

        # Average quality of evidence
        avg_quality = sum(e.quality_score for e in self.evidence) / len(self.evidence)

        # Agreement factor
        directions = [e.signal.direction.value for e in self.evidence]
        bullish = sum(1 for d in directions if d == "BULLISH")
        bearish = sum(1 for d in directions if d == "BEARISH")
        neutral = sum(1 for d in directions if d == "NEUTRAL")
        total = len(directions)

        agreement = max(bullish, bearish, neutral) / total if total > 0 else 0

        # Combine
        confidence = avg_quality * 0.6 + agreement * 0.4
        return min(1.0, confidence) * 100

    def get_conflict_level(self) -> ConflictLevel:
        """Determine conflict level"""
        directions = [e.signal.direction.value for e in self.evidence]
        bullish = sum(1 for d in directions if d == "BULLISH")
        bearish = sum(1 for d in directions if d == "BEARISH")
        total = len(directions)

        if total == 0:
            return ConflictLevel.NONE

        max_direction = max(bullish, bearish)
        ratio = max_direction / total

        if ratio >= 0.8:
            return ConflictLevel.NONE
        elif ratio >= 0.6:
            return ConflictLevel.LOW
        elif ratio >= 0.4:
            return ConflictLevel.MEDIUM
        else:
            return ConflictLevel.HIGH

    def get_supporting_engines(self) -> List[str]:
        """Get engines supporting the consensus direction"""
        if not self.evidence:
            return []

        consensus = self.get_consensus_direction()
        return [
            e.signal.engine_id
            for e in self.evidence
            if e.signal.direction.value == consensus
        ]

    def get_contradicting_engines(self) -> List[str]:
        """Get engines contradicting the consensus direction"""
        if not self.evidence:
            return []

        consensus = self.get_consensus_direction()
        return [
            e.signal.engine_id
            for e in self.evidence
            if e.signal.direction.value != consensus
            and e.signal.direction.value != "NEUTRAL"
        ]

    def get_drivers(self) -> List[str]:
        """Get aggregated drivers from all evidence"""
        driver_freq = {}
        for entry in self.evidence:
            for driver in entry.signal.drivers:
                driver_freq[driver] = driver_freq.get(driver, 0) + 1

        # Sort by frequency
        sorted_drivers = sorted(driver_freq.items(), key=lambda x: x[1], reverse=True)
        return [d for d, _ in sorted_drivers[:5]]

    def get_average_reliability(self) -> float:
        """Get average reliability of evidence"""
        if not self.evidence:
            return 0.0
        return sum(e.signal.reliability for e in self.evidence) / len(self.evidence)

    def get_freshness(self) -> float:
        """Get average freshness of evidence"""
        if not self.evidence:
            return 0.0
        return sum(e.signal.freshness for e in self.evidence) / len(self.evidence)

    def get_evidence_quality(self) -> float:
        """Get average evidence quality"""
        if not self.evidence:
            return 0.0
        return sum(e.signal.evidence_quality for e in self.evidence) / len(
            self.evidence
        )

    def to_evidence_object(self) -> Evidence:
        """Convert to Evidence schema object"""
        from ..schemas import Evidence

        return Evidence(
            signal_id=f"{self.entity}_{self.signal_type}_{datetime.utcnow().isoformat()}",
            entity=self.entity,
            signal_type=SignalType(self.signal_type),
            score=self.get_consensus_score(),
            direction=Direction(self.get_consensus_direction()),
            confidence=self.get_confidence(),
            source_engines=[e.signal.engine_id for e in self.evidence],
            source_count=len(self.evidence),
            average_reliability=self.get_average_reliability(),
            freshness=self.get_freshness(),
            evidence_quality=self.get_evidence_quality(),
            agreement_ratio=max(
                len(self.get_supporting_engines()) / len(self.evidence)
                if self.evidence
                else 0,
                0,
            ),
            conflict_level=self.get_conflict_level(),
            drivers=self.get_drivers(),
            raw_signals=[e.signal for e in self.evidence],
        )

    def get_supporting_engines_count(self) -> int:
        """Get count of supporting engines"""
        return len(self.get_supporting_engines())
