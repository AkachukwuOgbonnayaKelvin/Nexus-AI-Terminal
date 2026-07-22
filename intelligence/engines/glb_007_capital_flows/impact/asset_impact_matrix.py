"""
GLB-007 Capital Flows & Liquidity Intelligence Engine - Asset Impact Matrix Generator
"""

import logging
from typing import Dict

from intelligence.schemas.asset_impact import (
    AssetImpact,
    AssetImpactMatrix,
    AssetType,
    Direction,
    ImpactStatus,
    ImpactDriver,
)
from ..constants import ASSET_FLOW_EXPOSURE

logger = logging.getLogger(__name__)


class AssetImpactMatrixGenerator:
    """Generate canonical asset impact matrix from capital flows"""

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
        cls, flow_analysis: Dict, liquidity_analysis: Dict, confidence: float
    ) -> AssetImpactMatrix:
        """Generate asset impact matrix from capital flows and liquidity"""
        impacts = {}

        # Get key metrics
        flow_strength = flow_analysis.get("flow_strength", 0)
        flow_direction = flow_analysis.get("flow_direction", "NEUTRAL")
        liquidity_score = liquidity_analysis.get("liquidity_score", 50)
        liquidity_state = liquidity_analysis.get("liquidity_state", "NORMAL")
        funding_stress = liquidity_analysis.get("funding_stress", 50)
        dominant_flow = flow_analysis.get("dominant_flow", "RISK_ON")

        for asset in cls.SUPPORTED_ASSETS:
            impact = cls._calculate_asset_impact(
                asset,
                flow_strength,
                flow_direction,
                liquidity_score,
                liquidity_state,
                funding_stress,
                dominant_flow,
                confidence,
            )
            impacts[asset] = impact

        return AssetImpactMatrix(
            engine_id="GLB-007",
            engine_name="Capital Flows & Liquidity Intelligence Engine",
            impacts=impacts,
            covered_assets=list(impacts.keys()),
            overall_confidence=confidence,
            metadata={
                "flow_count": flow_analysis.get("flow_count", 0),
                "liquidity_score": liquidity_score,
                "flow_strength": flow_strength,
                "model_version": "1.0.0",
            },
        )

    @classmethod
    def _calculate_asset_impact(
        cls,
        asset: str,
        flow_strength: float,
        flow_direction: str,
        liquidity_score: float,
        liquidity_state: str,
        funding_stress: float,
        dominant_flow: str,
        confidence: float,
    ) -> AssetImpact:
        """Calculate impact for a single asset with normalized scores"""
        asset_type = cls._get_asset_type(asset)
        exposure = ASSET_FLOW_EXPOSURE.get(asset, {})

        if not exposure:
            return cls._neutral_impact(asset, confidence)

        # Calculate base score from flow strength
        base_score = 0.0
        drivers = []

        # Risk-on exposure
        if "risk_on" in exposure:
            risk_on_factor = exposure["risk_on"]
            if flow_direction == "INFLOW" or "RISK_ON" in dominant_flow:
                # Direct contribution with multiplier
                contribution = flow_strength * (risk_on_factor / 100) * 0.8
                base_score += contribution
                drivers.append("Risk-on capital inflow")
            elif "RISK_OFF" in dominant_flow:
                # Risk-off hurts risk-on assets
                contribution = -flow_strength * (abs(risk_on_factor) / 100) * 0.5
                base_score += contribution
                drivers.append("Risk-off pressure")

        # Risk-off exposure
        if "risk_off" in exposure:
            risk_off_factor = exposure["risk_off"]
            if (
                flow_direction == "OUTFLOW"
                or "RISK_OFF" in dominant_flow
                or "SAFE_HAVEN" in dominant_flow
            ):
                contribution = flow_strength * (abs(risk_off_factor) / 100) * 0.8
                if risk_off_factor > 0:
                    base_score += contribution
                    drivers.append("Safe-haven flow")
                else:
                    base_score -= contribution
                    drivers.append("Risk-off pressure")

        # Safe haven exposure
        if "safe_haven" in exposure:
            safe_factor = exposure["safe_haven"]
            if "SAFE_HAVEN" in dominant_flow or flow_direction == "INFLOW":
                contribution = flow_strength * (safe_factor / 100) * 0.7
                base_score += contribution
                if not drivers:
                    drivers.append("Safe-haven demand")

        # Commodity exposure
        if "commodity" in exposure:
            commodity_factor = exposure["commodity"]
            if "COMMODITY" in dominant_flow:
                contribution = flow_strength * (commodity_factor / 100) * 0.6
                base_score += contribution
                drivers.append("Commodity flow")

        # If no drivers, apply default based on asset type
        if not drivers:
            if asset_type == AssetType.FX:
                if "USD" in asset:
                    drivers.append("USD capital flow")
                else:
                    drivers.append("FX flow dynamics")
            elif asset_type == AssetType.COMMODITY:
                drivers.append("Commodity flow dynamics")
            else:
                drivers.append("Capital flow dynamics")

        # Apply liquidity adjustment
        liquidity_multiplier = 1.0
        if liquidity_score < 40:
            # Tight liquidity reduces risk asset scores
            if asset_type == AssetType.EQUITY:
                liquidity_multiplier = 0.7
            elif asset_type == AssetType.FX and asset not in [
                "USDCHF",
                "USDJPY",
                "XAUUSD",
            ]:
                liquidity_multiplier = 0.8
        elif liquidity_score > 70:
            # Abundant liquidity boosts risk assets
            if asset_type == AssetType.EQUITY:
                liquidity_multiplier = 1.3
            elif asset_type == AssetType.COMMODITY:
                liquidity_multiplier = 1.2

        # Apply funding stress adjustment
        stress_multiplier = 1.0
        if funding_stress > 60:
            if asset_type == AssetType.EQUITY:
                stress_multiplier = 0.7
            elif asset_type == AssetType.COMMODITY:
                stress_multiplier = 0.8
        elif funding_stress < 30:
            if asset_type == AssetType.EQUITY:
                stress_multiplier = 1.2

        # Calculate final score
        score = base_score * liquidity_multiplier * stress_multiplier

        # Ensure minimum impact for significant flows
        if abs(score) < 5 and flow_strength > 50:
            # Apply minimum impact
            sign = 1 if base_score > 0 else -1 if base_score < 0 else 0
            if sign != 0:
                score = sign * max(10, abs(score) * 1.5)

        # Limit to -100 to +100
        score = max(-100, min(100, score))
        direction = cls._get_direction(score)

        # Build drivers
        impact_drivers = []
        for d in drivers[:3]:
            impact_drivers.append(
                ImpactDriver(
                    name=d,
                    direction=direction,
                    strength=min(1.0, abs(score) / 100 + 0.2),
                )
            )

        # Confidence based on flow and liquidity confidence
        confidence_factor = min(1.0, (flow_strength / 100) * 0.6 + 0.3)
        final_confidence = confidence * 0.80 * confidence_factor

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
            engine_id="GLB-007",
            engine_name="Capital Flows & Liquidity Intelligence Engine",
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
            engine_id="GLB-007",
            engine_name="Capital Flows & Liquidity Intelligence Engine",
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
