"""
GLB-004 Economic Events Intelligence Engine - Asset Impact Matrix Generator
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

from ..constants import EVENT_DIRECTION_MAP, EventDirection

logger = logging.getLogger(__name__)


class AssetImpactMatrixGenerator:
    """Generate canonical asset impact matrix from events"""

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
    ]

    @classmethod
    def generate(
        cls, events: list[dict[str, Any]], confidence: float
    ) -> AssetImpactMatrix:
        """Generate asset impact matrix from events"""
        impacts = {}

        # Calculate impact for each asset
        for asset in cls.SUPPORTED_ASSETS:
            impact = cls._calculate_asset_impact(asset, events, confidence)
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-004",
            engine_name="Economic Events Intelligence Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={"event_count": len(events), "model_version": "1.0.0"},
        )

    @classmethod
    def _calculate_asset_impact(
        cls, asset: str, events: list[dict], confidence: float
    ) -> AssetImpact:
        """Calculate impact for a single asset"""
        asset_type = cls._get_asset_type(asset)

        # Calculate base impact
        base_score = 0.0
        event_references = []
        drivers = []

        for event in events:
            score, driver = cls._calculate_event_impact(asset, event)
            if abs(score) > 0:
                base_score += score
                event_references.append(event.get("event", "Unknown"))
                if driver:
                    drivers.append(driver)

        # Normalize score
        if event_references:
            base_score = base_score / len(event_references)

        # Limit to -100 to +100
        score = max(-100, min(100, base_score))
        direction = cls._get_direction(score)

        # Build drivers
        impact_drivers = []
        for d in drivers[:3]:
            impact_drivers.append(
                ImpactDriver(name=d, direction=direction, strength=0.7)
            )

        return AssetImpact(
            asset=asset,
            asset_type=asset_type,
            score=score,
            direction=direction,
            confidence=confidence * 0.75,
            status=ImpactStatus.ANALYZED
            if event_references
            else ImpactStatus.NOT_COVERED,
            drivers=impact_drivers,
            relevance=0.70 if event_references else 0.1,
            engine_id="GLB-004",
            engine_name="Economic Events Intelligence Engine",
        )

    @classmethod
    def _calculate_event_impact(cls, asset: str, event: dict) -> tuple:
        """Calculate impact of a single event on an asset"""
        event_name = event.get("event", "")
        surprise = event.get("deviation", 0)
        # currency = ...  # Unused

        if abs(surprise) < 0.1:
            return 0, None

        # Find direction map
        direction_map = cls._find_direction_map(event_name)
        if not direction_map:
            return 0, None

        # Determine direction
        direction = "higher" if surprise > 0 else "lower"
        if direction not in direction_map:
            return 0, None

        # Get asset impact
        asset_impacts = direction_map[direction]

        # Find matching asset impact
        for key, value in asset_impacts.items():
            if key in asset or asset in key:
                if value == EventDirection.BULLISH.value:
                    score = 20
                    driver = f"{event_name}: {direction} than expected"
                    return score, driver
                elif value == EventDirection.BEARISH.value:
                    score = -20
                    driver = f"{event_name}: {direction} than expected"
                    return score, driver

        return 0, None

    @classmethod
    def _find_direction_map(cls, event_name: str) -> dict:
        """Find direction map for an event"""
        for key, direction_map in EVENT_DIRECTION_MAP.items():
            if key.lower() in event_name.lower() or event_name.lower() in key.lower():
                return direction_map
        return {}

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
        commodities = ["XAUUSD", "XAGUSD"]
        equities = ["US500", "US100", "US30", "GER40", "UK100", "JP225"]

        if asset in fx_pairs:
            return AssetType.FX
        elif asset in commodities:
            return AssetType.COMMODITY
        elif asset in equities:
            return AssetType.EQUITY
        return AssetType.FX
