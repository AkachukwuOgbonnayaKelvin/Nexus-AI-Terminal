"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Asset Impact Matrix Generator
"""

import logging

from intelligence.schemas.asset_impact import (
    AssetImpact,
    AssetImpactMatrix,
    AssetType,
    Direction,
    ImpactDriver,
    ImpactStatus,
)

logger = logging.getLogger(__name__)


class AssetImpactMatrixGenerator:
    """Generate canonical asset impact matrix from historical analogues"""

    @classmethod
    def generate(
        cls,
        outcome_analyses: dict,
        cross_asset_confirmation: dict,
        analogue_quality: dict,
        confidence: float,
        available_assets: list[str] = None,
    ) -> AssetImpactMatrix:
        """Generate asset impact matrix from historical analogues"""
        impacts = {}

        # Get asset outcomes from the analyses
        asset_outcomes = outcome_analyses.get("asset_outcomes", {})

        if not asset_outcomes:
            logger.warning("No asset outcomes found")
            return AssetImpactMatrix(
                engine_id="GLB-009",
                engine_name="Market Memory & Historical Analogy Intelligence Engine",
                impacts={},
                covered_assets=[],
                overall_confidence=confidence,
                metadata={"error": "No asset outcomes available"},
            )

        # Determine which assets to analyze
        if available_assets:
            assets_to_analyze = [a for a in available_assets if a in asset_outcomes]
        else:
            assets_to_analyze = list(asset_outcomes.keys())

        if not assets_to_analyze:
            logger.warning("No matching assets found")
            return AssetImpactMatrix(
                engine_id="GLB-009",
                engine_name="Market Memory & Historical Analogy Intelligence Engine",
                impacts={},
                covered_assets=[],
                overall_confidence=confidence,
                metadata={"error": "No matching assets"},
            )

        # Get quality metrics
        quality = analogue_quality.get("quality", "MODERATE")
        best_match = analogue_quality.get("best_match", 50)
        match_confidence = analogue_quality.get("match_confidence", 50)

        # Process each asset
        for asset in assets_to_analyze:
            asset_outcome = asset_outcomes.get(asset, {})

            # If no outcome data, skip
            if not asset_outcome or asset_outcome.get("status") != "OPERATIONAL":
                continue

            # Calculate impact score
            impact = cls._calculate_asset_impact(
                asset, asset_outcome, quality, best_match, match_confidence, confidence
            )
            if impact:
                impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-009",
            engine_name="Market Memory & Historical Analogy Intelligence Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "analogues_used": len(outcome_analyses.get("analogues", [])),
                "assets_processed": len(impacts),
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _calculate_asset_impact(
        cls,
        asset: str,
        asset_outcome: dict,
        quality: str,
        best_match: float,
        match_confidence: float,
        confidence: float,
    ) -> AssetImpact:
        """Calculate impact for a single asset from its outcome data"""
        asset_type = cls._get_asset_type(asset)

        # Extract outcome distribution
        distribution = asset_outcome.get("outcome_distribution", {})
        bullish_pct = distribution.get("BULLISH", 0) * 100
        bearish_pct = distribution.get("BEARISH", 0) * 100
        # neutral_pct = ...  # Unused

        # Get mean return
        mean_return = asset_outcome.get("mean_return", 0)
        # median_return = ...  # Unused
        sample_count = asset_outcome.get("sample_count", 0)

        # Calculate directional edge (-100 to +100)
        directional_edge = bullish_pct - bearish_pct

        # Calculate return factor (-100 to +100)
        # Scale mean return by 20 (typical returns are around 1-2%)
        return_factor = mean_return * 20
        return_factor = max(-100, min(100, return_factor))

        # Calculate quality factor (0 to 1)
        quality_factor = 0.5
        if quality == "HIGH":
            quality_factor = 1.0
        elif quality == "MODERATE":
            quality_factor = 0.75
        elif quality == "LOW":
            quality_factor = 0.5

        # Calculate match factor (0 to 1)
        match_factor = best_match / 100

        # Calculate sample penalty
        # More samples = higher confidence
        sample_penalty = min(1.0, sample_count / 30)

        # CALCULATE FINAL SCORE (-100 to +100)
        # Combine directional edge, return factor, and quality
        if directional_edge > 0:
            # Bullish case
            base_score = directional_edge * 0.50
            score = base_score + (return_factor * 0.20) + (quality_factor * 10)
        else:
            # Bearish case
            base_score = directional_edge * 0.50
            score = base_score + (return_factor * 0.20) - (quality_factor * 10)

        # Apply sample penalty
        score = score * (0.5 + 0.5 * sample_penalty)

        # Apply match factor
        score = score * (0.7 + 0.3 * match_factor)

        # Clamp
        score = max(-100, min(100, score))
        direction = cls._get_direction(score)

        # Calculate confidence (0-100)
        # Based on: sample size, match quality, directional clarity
        directional_clarity = abs(directional_edge) / 100
        confidence_base = (
            (sample_penalty * 0.4) + (match_factor * 0.3) + (directional_clarity * 0.3)
        )
        final_confidence = confidence_base * confidence * 0.85
        final_confidence = min(95, max(10, final_confidence))

        # Build drivers
        drivers = [
            f"Bullish: {bullish_pct:.0f}% / Bearish: {bearish_pct:.0f}%",
            f"Mean Return: {mean_return:+.2f}%",
            f"Sample: {sample_count} analogues",
            f"Quality: {quality}",
        ]

        impact_drivers = []
        for d in drivers[:3]:
            impact_drivers.append(
                ImpactDriver(
                    name=d,
                    direction=direction,
                    strength=min(1.0, abs(score) / 100 + 0.2),
                )
            )

        return AssetImpact(
            asset=asset,
            asset_type=asset_type,
            score=score,
            direction=direction,
            confidence=final_confidence,
            status=ImpactStatus.ANALYZED
            if abs(score) > 5
            else ImpactStatus.NOT_COVERED,
            drivers=impact_drivers,
            relevance=0.70 if abs(score) > 5 else 0.20,
            engine_id="GLB-009",
            engine_name="Market Memory & Historical Analogy Intelligence Engine",
        )

    @classmethod
    def _neutral_impact(cls, asset: str, confidence: float) -> AssetImpact:
        return AssetImpact(
            asset=asset,
            asset_type=cls._get_asset_type(asset),
            score=0,
            direction=Direction.NEUTRAL,
            confidence=confidence * 0.1,
            status=ImpactStatus.NOT_COVERED,
            drivers=[],
            relevance=0.1,
            engine_id="GLB-009",
            engine_name="Market Memory & Historical Analogy Intelligence Engine",
        )

    @classmethod
    def _get_direction(cls, score: float) -> Direction:
        if score > 10:
            return Direction.BULLISH
        elif score < -10:
            return Direction.BEARISH
        return Direction.NEUTRAL

    @classmethod
    def _get_asset_type(cls, asset: str) -> AssetType:
        fx = ["AUDUSD", "AUDCAD", "AUDJPY", "AUDNZD", "CADCHF", "CADJPY", "CHFJPY"]
        commodities = ["CL=F", "BZ=F", "CLNX.ES"]

        if asset in fx:
            return AssetType.FX
        elif asset in commodities:
            return AssetType.COMMODITY
        return AssetType.FX
