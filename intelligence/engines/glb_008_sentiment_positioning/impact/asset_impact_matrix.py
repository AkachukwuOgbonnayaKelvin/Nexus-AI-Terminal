"""
GLB-008 Sentiment & Positioning Intelligence Engine - Asset Impact Matrix Generator
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

from ..constants import ASSET_SENTIMENT_EXPOSURE

logger = logging.getLogger(__name__)


class AssetImpactMatrixGenerator:
    """Generate canonical asset impact matrix from sentiment and positioning"""

    SUPPORTED_ASSETS = [
        "EURUSD",
        "GBPUSD",
        "USDJPY",
        "AUDUSD",
        "NZDUSD",
        "USDCAD",
        "USDCHF",
        "XAUUSD",
        "XAGUSD",
        "US500",
        "US100",
        "US30",
        "GER40",
        "UK100",
        "JP225",
        "WTI",
        "BRENT",
    ]

    @classmethod
    def generate(
        cls,
        sentiment_analysis: dict,
        positioning_analysis: dict,
        crowding_analysis: dict,
        divergence_analysis: dict,
        confidence: float,
    ) -> AssetImpactMatrix:
        """Generate asset impact matrix from sentiment and positioning"""
        impacts = {}

        # Get key metrics
        sentiment_score = sentiment_analysis.get("sentiment_score", 50)
        sentiment_state = sentiment_analysis.get("sentiment_state", "NEUTRAL")
        positioning_bias = positioning_analysis.get("overall_bias", "NEUTRAL")
        crowding_score = crowding_analysis.get("crowding_score", 50)
        divergence_detected = divergence_analysis.get("divergence_detected", False)

        for asset in cls.SUPPORTED_ASSETS:
            impact = cls._calculate_asset_impact(
                asset,
                sentiment_score,
                sentiment_state,
                positioning_bias,
                crowding_score,
                divergence_detected,
                confidence,
            )
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-008",
            engine_name="Sentiment & Positioning Intelligence Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "sentiment_score": sentiment_score,
                "crowding_score": crowding_score,
                "divergence_detected": divergence_detected,
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _calculate_asset_impact(
        cls,
        asset: str,
        sentiment_score: float,
        sentiment_state: str,
        positioning_bias: str,
        crowding_score: float,
        divergence_detected: bool,
        confidence: float,
    ) -> AssetImpact:
        """Calculate impact for a single asset"""
        asset_type = cls._get_asset_type(asset)
        exposure = ASSET_SENTIMENT_EXPOSURE.get(asset, 0.0)

        if exposure == 0.0:
            return cls._neutral_impact(asset, confidence)

        # Calculate base score from sentiment
        normalized_sentiment = (sentiment_score - 50) / 50  # -1 to +1
        base_score = normalized_sentiment * exposure * 50

        # Adjust for positioning bias
        if positioning_bias == "LONG" and exposure > 0:
            base_score = (
                base_score * 1.1
            )  # Long positioning amplifies bullish sentiment
        elif positioning_bias == "SHORT" and exposure < 0:
            base_score = (
                base_score * 1.1
            )  # Short positioning amplifies bearish sentiment
        elif positioning_bias == "LONG" and exposure < 0:
            base_score = base_score * 0.8  # Long positioning dampens bearish sentiment
        elif positioning_bias == "SHORT" and exposure > 0:
            base_score = base_score * 0.8  # Short positioning dampens bullish sentiment

        # Adjust for crowding
        if crowding_score > 70:
            # High crowding = reduce conviction
            base_score = base_score * 0.7
        elif crowding_score > 50:
            base_score = base_score * 0.85

        # Adjust for divergence
        if divergence_detected:
            # Divergence creates contrarian opportunity
            base_score = base_score * 0.6
            confidence = confidence * 0.6

        # Limit to -100 to +100
        score = max(-100, min(100, base_score))
        direction = cls._get_direction(score)

        # Build drivers
        drivers = []
        if sentiment_score > 60:
            drivers.append("Bullish sentiment")
        elif sentiment_score < 40:
            drivers.append("Bearish sentiment")
        else:
            drivers.append("Neutral sentiment")

        if crowding_score > 70:
            drivers.append("High crowding")

        if divergence_detected:
            drivers.append("Sentiment-positioning divergence")

        impact_drivers = []
        for d in drivers[:3]:
            impact_drivers.append(
                ImpactDriver(
                    name=d,
                    direction=direction,
                    strength=min(1.0, abs(score) / 100 + 0.2),
                )
            )

        # Confidence factor
        confidence_factor = min(1.0, (abs(sentiment_score - 50) / 50) * 0.5 + 0.3)
        if divergence_detected:
            confidence_factor = confidence_factor * 0.6
        final_confidence = confidence * 0.75 * confidence_factor

        return AssetImpact(
            asset=asset,
            asset_type=asset_type,
            score=score,
            direction=direction,
            confidence=min(95, final_confidence),
            status=ImpactStatus.ANALYZED
            if abs(score) > 5
            else ImpactStatus.NOT_COVERED,
            drivers=impact_drivers,
            relevance=0.70 if abs(score) > 5 else 0.20,
            engine_id="GLB-008",
            engine_name="Sentiment & Positioning Intelligence Engine",
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
            engine_id="GLB-008",
            engine_name="Sentiment & Positioning Intelligence Engine",
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
        fx_pairs = [
            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "AUDUSD",
            "NZDUSD",
            "USDCAD",
            "USDCHF",
        ]
        commodities = ["XAUUSD", "XAGUSD", "WTI", "BRENT"]
        equities = ["US500", "US100", "US30", "GER40", "UK100", "JP225"]

        if asset in fx_pairs:
            return AssetType.FX
        elif asset in commodities:
            return AssetType.COMMODITY
        elif asset in equities:
            return AssetType.EQUITY
        return AssetType.FX
