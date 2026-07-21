"""
Global Intelligence Hub - Aggregator v2.0

Hardened version with:
- NOT_COVERED distinct from NEUTRAL
- Proper confidence calculation
- Conflict detection
- Data freshness tracking
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from intelligence.schemas.asset_impact import AssetImpactMatrix, Direction, ImpactStatus

logger = logging.getLogger(__name__)


@dataclass
class EngineContribution:
    """Contribution from a single engine for an asset"""

    engine_id: str
    engine_name: str
    score: float
    direction: str
    weight: float
    confidence: float
    status: str
    drivers: List[str]
    generated_at: Optional[datetime] = None


@dataclass
class AssetConsensus:
    """Consensus for a single asset"""

    asset: str
    asset_type: str
    consensus_score: float
    display_score: float
    direction: str
    confidence: float

    # Agreement metrics
    agreement: Dict[str, int]
    agreement_ratio: float

    # Conflict detection
    has_conflict: bool
    conflict_level: str  # NONE, LOW, MEDIUM, HIGH

    # Contributions
    contributions: Dict[str, EngineContribution]

    # Metadata
    top_drivers: List[str]
    analyzed_engines: int
    total_engines: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class HubAggregator:
    """Aggregates multiple Asset Impact Matrices into a Global Asset Impact Map."""

    # Default weights for each engine (can be overridden)
    DEFAULT_WEIGHTS = {
        "GLB-001": 0.30,
        "GLB-002": 0.35,
        "GLB-003": 0.35,
    }

    # Engine reliability scores (0-100)
    ENGINE_RELIABILITY = {
        "GLB-001": 85,
        "GLB-002": 80,
        "GLB-003": 75,
    }

    def __init__(self):
        self.engine_weights = self.DEFAULT_WEIGHTS.copy()
        self.engine_reliability = self.ENGINE_RELIABILITY.copy()
        self.matrices: Dict[str, AssetImpactMatrix] = {}
        self.last_aggregation: Optional[datetime] = None

    def register_matrix(self, matrix: AssetImpactMatrix) -> None:
        """Register an engine's Asset Impact Matrix."""
        self.matrices[matrix.engine_id] = matrix
        logger.info(
            f"Registered matrix from {matrix.engine_id} with {len(matrix.impacts)} assets"
        )

    def set_weight(self, engine_id: str, weight: float) -> None:
        """Set weight for a specific engine."""
        self.engine_weights[engine_id] = weight

    def set_reliability(self, engine_id: str, reliability: float) -> None:
        """Set reliability score for a specific engine."""
        self.engine_reliability[engine_id] = reliability

    def aggregate(self) -> Dict[str, AssetConsensus]:
        """Aggregate all registered matrices into consensus for each asset."""
        if not self.matrices:
            logger.warning("No matrices registered")
            return {}

        self.last_aggregation = datetime.utcnow()

        all_assets = set()
        for matrix in self.matrices.values():
            all_assets.update(matrix.impacts.keys())

        consensus = {}
        for asset in sorted(all_assets):
            consensus[asset] = self._build_asset_consensus(asset)

        return consensus

    def _build_asset_consensus(self, asset: str) -> AssetConsensus:
        """Build consensus for a single asset."""
        contributions = {}
        analyzed = []  # List of (score, weight, confidence, reliability)
        directions = []
        all_drivers = []
        asset_type = "UNKNOWN"

        for engine_id, matrix in self.matrices.items():
            if asset not in matrix.impacts:
                continue

            impact = matrix.impacts[asset]
            weight = self.engine_weights.get(engine_id, 0.20)
            reliability = self.engine_reliability.get(engine_id, 70)

            # Track asset type from first analyzed asset
            if impact.asset_type and impact.asset_type.value:
                asset_type = impact.asset_type.value

            # Handle different statuses
            if impact.status == ImpactStatus.ANALYZED:
                # This engine has valid analysis
                contribution = EngineContribution(
                    engine_id=engine_id,
                    engine_name=matrix.engine_name,
                    score=impact.score,
                    direction=impact.direction.value,
                    weight=weight,
                    confidence=impact.confidence,
                    status="ANALYZED",
                    drivers=[d.name for d in impact.drivers],
                    generated_at=impact.generated_at,
                )
                contributions[engine_id] = contribution
                analyzed.append((impact.score, weight, impact.confidence, reliability))
                directions.append(impact.direction.value)
                all_drivers.extend([d.name for d in impact.drivers])

            elif impact.status == ImpactStatus.NOT_COVERED:
                # Engine doesn't cover this asset - exclude entirely
                contribution = EngineContribution(
                    engine_id=engine_id,
                    engine_name=matrix.engine_name,
                    score=0,
                    direction="NOT_COVERED",
                    weight=weight,
                    confidence=0,
                    status="NOT_COVERED",
                    drivers=[],
                )
                contributions[engine_id] = contribution

            else:  # INSUFFICIENT_DATA
                contribution = EngineContribution(
                    engine_id=engine_id,
                    engine_name=matrix.engine_name,
                    score=0,
                    direction="INSUFFICIENT_DATA",
                    weight=weight,
                    confidence=0.1,
                    status="INSUFFICIENT_DATA",
                    drivers=[],
                )
                contributions[engine_id] = contribution

        # If no engine analyzed this asset
        if not analyzed:
            return AssetConsensus(
                asset=asset,
                asset_type=asset_type,
                consensus_score=0,
                display_score=50.0,
                direction="NEUTRAL",
                confidence=0.0,
                agreement={"bullish": 0, "bearish": 0, "neutral": 0},
                agreement_ratio=0.0,
                has_conflict=False,
                conflict_level="NONE",
                contributions=contributions,
                top_drivers=[],
                analyzed_engines=0,
                total_engines=len(self.matrices),
            )

        # Calculate weighted consensus (-100 to +100)
        total_weight = sum(w for _, w, _, _ in analyzed)
        if total_weight <= 0:
            consensus_score = 0
        else:
            # Apply reliability as a multiplier to the contribution
            weighted_sum = sum(s * w * (r / 100) for s, w, _, r in analyzed)
            total_reliability_weight = sum(w * (r / 100) for _, w, _, r in analyzed)
            consensus_score = (
                weighted_sum / total_reliability_weight
                if total_reliability_weight > 0
                else 0
            )

        # Determine direction
        if consensus_score > 10:
            direction = Direction.BULLISH.value
        elif consensus_score < -10:
            direction = Direction.BEARISH.value
        else:
            direction = Direction.NEUTRAL.value

        # Calculate agreement
        bullish = sum(1 for d in directions if d == Direction.BULLISH.value)
        bearish = sum(1 for d in directions if d == Direction.BEARISH.value)
        neutral = sum(1 for d in directions if d == Direction.NEUTRAL.value)
        total_dir = len(directions)
        agreement_ratio = (
            max(bullish, bearish, neutral) / total_dir if total_dir > 0 else 0
        )

        agreement = {"bullish": bullish, "bearish": bearish, "neutral": neutral}

        # Detect conflict
        has_conflict = (bullish > 0 and bearish > 0) or (
            bullish > 0 and neutral > 0 and bearish > 0
        )
        conflict_level = self._determine_conflict_level(
            bullish, bearish, neutral, total_dir
        )

        # Calculate confidence (with reliability, agreement, and conflict penalty)
        avg_confidence = (
            sum(c for _, _, c, _ in analyzed) / len(analyzed) if analyzed else 50
        )
        avg_reliability = (
            sum(r for _, _, _, r in analyzed) / len(analyzed) if analyzed else 70
        )

        # Base confidence from average confidence and reliability
        base_confidence = (avg_confidence * 0.5) + (avg_reliability * 0.3)

        # Adjust for agreement
        agreement_factor = agreement_ratio  # 0.0 to 1.0

        # Apply conflict penalty
        conflict_penalty = 0.0
        if has_conflict:
            conflict_penalty = (
                0.15 * (bearish + bullish) / total_dir if total_dir > 0 else 0.0
            )

        # Calculate final confidence
        confidence = (base_confidence * 0.5) + (agreement_factor * 100 * 0.5)
        confidence = confidence * (1 - conflict_penalty)
        confidence = min(95, max(0, confidence))

        # Top drivers
        driver_freq = {}
        for d in all_drivers:
            driver_freq[d] = driver_freq.get(d, 0) + 1
        top_drivers = sorted(
            driver_freq.keys(), key=lambda x: driver_freq[x], reverse=True
        )[:5]

        return AssetConsensus(
            asset=asset,
            asset_type=asset_type,
            consensus_score=consensus_score,
            display_score=50 + (consensus_score / 2),
            direction=direction,
            confidence=confidence,
            agreement=agreement,
            agreement_ratio=agreement_ratio,
            has_conflict=has_conflict,
            conflict_level=conflict_level,
            contributions=contributions,
            top_drivers=top_drivers,
            analyzed_engines=len(analyzed),
            total_engines=len(self.matrices),
            metadata={
                "raw_scores": [s for s, _, _, _ in analyzed],
                "weights": [w for _, w, _, _ in analyzed],
                "reliabilities": [r for _, _, _, r in analyzed],
                "confidences": [c for _, _, c, _ in analyzed],
            },
        )

    def _determine_conflict_level(
        self, bullish: int, bearish: int, neutral: int, total: int
    ) -> str:
        """Determine conflict level based on direction distribution."""
        if total == 0:
            return "NONE"

        # If all agree, no conflict
        if bullish == total or bearish == total or neutral == total:
            return "NONE"

        # If there's at least one of each, high conflict
        if bullish > 0 and bearish > 0 and neutral > 0:
            return "HIGH"

        # If there's both bullish and bearish (no neutral), medium conflict
        if bullish > 0 and bearish > 0:
            return "MEDIUM"

        # If there's a mix of one direction and neutral
        return "LOW"

    def get_asset_map(
        self, asset_type: Optional[str] = None
    ) -> Dict[str, AssetConsensus]:
        """Get the Global Asset Impact Map, optionally filtered by asset type."""
        all_consensus = self.aggregate()

        if asset_type:
            return {
                asset: consensus
                for asset, consensus in all_consensus.items()
                if consensus.asset_type == asset_type
            }

        return all_consensus

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the aggregation."""
        consensus = self.aggregate()

        if not consensus:
            return {"status": "NO_DATA"}

        bullish = sum(
            1 for c in consensus.values() if c.direction == Direction.BULLISH.value
        )
        bearish = sum(
            1 for c in consensus.values() if c.direction == Direction.BEARISH.value
        )
        neutral = sum(
            1 for c in consensus.values() if c.direction == Direction.NEUTRAL.value
        )

        # Count by type
        types = {}
        for c in consensus.values():
            types[c.asset_type] = types.get(c.asset_type, 0) + 1

        # Count conflicts
        conflicts = {"NONE": 0, "LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for c in consensus.values():
            conflicts[c.conflict_level] = conflicts.get(c.conflict_level, 0) + 1

        sorted_by_score = sorted(
            consensus.values(), key=lambda x: x.display_score, reverse=True
        )
        strongest = sorted_by_score[0] if sorted_by_score else None
        weakest = sorted_by_score[-1] if sorted_by_score else None

        return {
            "total_assets": len(consensus),
            "bullish": bullish,
            "bearish": bearish,
            "neutral": neutral,
            "by_type": types,
            "conflicts": conflicts,
            "strongest": {
                "asset": strongest.asset if strongest else None,
                "score": strongest.display_score if strongest else 0,
                "direction": strongest.direction if strongest else None,
                "confidence": strongest.confidence if strongest else 0,
            }
            if strongest
            else None,
            "weakest": {
                "asset": weakest.asset if weakest else None,
                "score": weakest.display_score if weakest else 0,
                "direction": weakest.direction if weakest else None,
                "confidence": weakest.confidence if weakest else 0,
            }
            if weakest
            else None,
            "engine_count": len(self.matrices),
            "engines": list(self.matrices.keys()),
            "last_aggregation": self.last_aggregation.isoformat()
            if self.last_aggregation
            else None,
        }

    def health_check(self) -> Dict[str, Any]:
        """Check aggregator health."""
        return {
            "status": "OPERATIONAL",
            "registered_engines": len(self.matrices),
            "engine_ids": list(self.matrices.keys()),
            "last_aggregation": self.last_aggregation.isoformat()
            if self.last_aggregation
            else None,
        }
