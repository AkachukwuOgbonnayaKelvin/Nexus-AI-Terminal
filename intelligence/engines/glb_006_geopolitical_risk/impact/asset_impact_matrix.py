"""
GLB-006 Geopolitical Risk Intelligence Engine - Asset Impact Matrix Generator
"""

import logging
from typing import Any

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
    """Generate canonical asset impact matrix from geopolitical risk"""

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
        "NGAS",
        "COPPER",
    ]

    # Asset exposure: direction and magnitude (-1.0 to +1.0)
    # Positive = bullish with risk, Negative = bearish with risk
    ASSET_EXPOSURE = {
        # Safe havens (positive)
        "XAUUSD": 0.95,
        "USDCHF": 0.85,
        "USDJPY": 0.80,
        # Risk currencies (negative)
        "AUDUSD": -0.80,
        "NZDUSD": -0.75,
        "USDCAD": -0.60,
        "EURUSD": -0.50,
        "GBPUSD": -0.45,
        # Commodities
        "WTI": 0.70,
        "BRENT": 0.70,
        "XAGUSD": 0.50,
        "NGAS": 0.55,
        "COPPER": -0.50,
        # Equities (negative)
        "US500": -0.85,
        "US100": -0.90,
        "US30": -0.80,
        "GER40": -0.80,
        "UK100": -0.75,
        "JP225": -0.70,
    }

    @classmethod
    def generate(
        cls,
        events: list[Any],
        global_state: dict,
        transmission: dict,
        confidence: float,
        diagnostic: bool = False,
    ) -> AssetImpactMatrix:
        """Generate asset impact matrix from geopolitical risk"""
        impacts = {}

        # CRITICAL FIX: Get risk score from global_state
        risk_score = global_state.get("global_risk_score", 0)
        if risk_score == 0:
            # Fallback: try alternative key
            risk_score = global_state.get("global_geopolitical_risk", 0)

        # Get channel strength from transmission
        channels = transmission.get("channels", {})

        # Calculate overall channel strength (weighted average of all channels)
        if channels:
            total_strength = sum(channels.values())
            channel_strength = total_strength / len(channels) if channels else 0.5
        else:
            channel_strength = 0.5  # Default fallback

        # Ensure channel_strength is reasonable
        channel_strength = max(0.1, min(1.0, channel_strength))

        # Diagnostic
        if diagnostic:
            print("\n" + "=" * 70)
            print("GLB-006 ASSET IMPACT DIAGNOSTIC")
            print("=" * 70)
            print(f"Risk Score (from global_state): {risk_score:.1f}")
            print(f"Channel Strength: {channel_strength:.3f}")
            print(f"Channels: {channels}")
            print(f"Asset Exposure Count: {len(cls.ASSET_EXPOSURE)}")
            print("=" * 70)

        for asset in cls.SUPPORTED_ASSETS:
            impact = cls._calculate_asset_impact(
                asset, risk_score, channel_strength, confidence, diagnostic
            )
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-006",
            engine_name="Geopolitical Risk Intelligence Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "event_count": len(events),
                "risk_score": risk_score,
                "channel_strength": channel_strength,
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _calculate_asset_impact(
        cls,
        asset: str,
        risk_score: float,
        channel_strength: float,
        confidence: float,
        diagnostic: bool = False,
    ) -> AssetImpact:
        """
        Calculate impact for a single asset.

        Formula:
            Impact Score = Risk Score × Channel Strength × Asset Exposure
        """
        asset_type = cls._get_asset_type(asset)

        # Get exposure for this asset (-1.0 to +1.0)
        exposure = cls.ASSET_EXPOSURE.get(asset, 0.0)

        if exposure == 0.0:
            return cls._neutral_impact(asset, confidence)

        # DIRECT CALCULATION
        raw_score = risk_score * channel_strength * exposure
        score = max(-100, min(100, raw_score))
        direction = cls._get_direction(score)

        # Diagnostic output
        if diagnostic and asset in ["XAUUSD", "US100", "US500", "AUDUSD", "WTI"]:
            print(f"\n{'=' * 50}")
            print(f"ASSET: {asset}")
            print(f"{'=' * 50}")
            print(f"  Risk Score: {risk_score:.1f}")
            print(f"  Channel Strength: {channel_strength:.3f}")
            print(f"  Exposure: {exposure:+.2f}")
            print(f"  Raw Score: {raw_score:.1f}")
            print(f"  Final Score: {score:.1f}")
            print(f"  Direction: {direction.value}")
            print(f"{'=' * 50}")

        # Build drivers
        drivers = []
        if exposure > 0:
            drivers.append(f"Safe-haven/positive exposure: {exposure:+.2f}")
        else:
            drivers.append(f"Risk-off/negative exposure: {exposure:+.2f}")
        drivers.append(f"Channel strength: {channel_strength:.2f}")

        impact_drivers = []
        for d in drivers[:3]:
            impact_drivers.append(
                ImpactDriver(
                    name=d,
                    direction=direction,
                    strength=min(1.0, abs(score) / 100 + 0.2),
                )
            )

        # Confidence - separate from score
        confidence_factor = min(1.0, (risk_score / 100) * 0.5 + 0.3)
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
            engine_id="GLB-006",
            engine_name="Geopolitical Risk Intelligence Engine",
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
            engine_id="GLB-006",
            engine_name="Geopolitical Risk Intelligence Engine",
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
        commodities = ["XAUUSD", "XAGUSD", "WTI", "BRENT", "NGAS", "COPPER"]
        equities = ["US500", "US100", "US30", "GER40", "UK100", "JP225"]

        if asset in fx_pairs:
            return AssetType.FX
        elif asset in commodities:
            return AssetType.COMMODITY
        elif asset in equities:
            return AssetType.EQUITY
        return AssetType.FX
