"""
GLB-001 Market Regime Engine - Report Generator
"""

import logging
from typing import Any

from .constants import SUPPORTED_ASSETS, MarketRegime, RegimeAlignment, TransitionState
from .schemas import (
    AssetRegimeContext,
    MarketDimension,
    RegimeDriver,
    RegimeEvidence,
    RegimeReport,
    RegimeRisk,
    RegimeSignal,
)

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates the final EngineReport in Universal Contract format."""

    def generate(
        self,
        primary_regime: MarketRegime,
        secondary_regime: MarketRegime,
        transition_state: TransitionState,
        regime_score: float,
        confidence: float,
        dimensions: list[MarketDimension],
        regime_probabilities: dict[str, float],
        signals: list[RegimeSignal],
        evidence: list[RegimeEvidence],
        risks: list[RegimeRisk],
        drivers: list[RegimeDriver],
        normalized_data: dict[str, Any],
    ) -> RegimeReport:
        asset_context = self._build_asset_context(
            primary_regime, dimensions, normalized_data
        )

        metadata = {
            "calculation_time_ms": 0,
            "input_count": len(normalized_data),
            "model_version": "1.0.0",
            "data_freshness": self._determine_freshness(normalized_data),
            "dimension_count": len(dimensions),
            "evidence_count": len(evidence),
            "risk_count": len(risks),
        }

        return RegimeReport(
            primary_regime=primary_regime,
            secondary_regime=secondary_regime,
            transition_state=transition_state,
            regime_score=regime_score,
            confidence=confidence,
            dimensions=dimensions,
            regime_probabilities=regime_probabilities,
            signals=signals,
            evidence=evidence,
            risks=risks,
            drivers=drivers,
            asset_context=asset_context,
            metadata=metadata,
        )

    def _build_asset_context(
        self,
        primary_regime: MarketRegime,
        dimensions: list[MarketDimension],
        normalized_data: dict[str, Any],
    ) -> dict[str, AssetRegimeContext]:
        context = {}
        dimension_dict = {d.name: d for d in dimensions}
        for asset in SUPPORTED_ASSETS:
            context[asset] = self._asset_context_for(
                asset, primary_regime, dimension_dict, normalized_data
            )
        return context

    def _asset_context_for(
        self,
        asset: str,
        primary_regime: MarketRegime,
        dimensions: dict[str, MarketDimension],
        normalized_data: dict[str, Any],
    ) -> AssetRegimeContext:
        alignment = self._determine_alignment(asset, primary_regime, dimensions)
        score = self._calculate_asset_score(asset, dimensions)
        primary_factor = self._determine_primary_factor(asset, dimensions)
        confidence = self._calculate_asset_confidence(asset, normalized_data)

        return AssetRegimeContext(
            asset=asset,
            regime_alignment=alignment,
            regime_score=score,
            confidence=confidence,
            primary_factor=primary_factor,
        )

    def _determine_alignment(
        self, asset: str, regime: MarketRegime, dimensions: dict[str, MarketDimension]
    ) -> RegimeAlignment:
        if regime == MarketRegime.RISK_ON:
            if asset in ["XAUUSD", "XAGUSD", "USDJPY"]:
                return RegimeAlignment.NEGATIVE
            elif asset in ["US500", "US100", "US30", "GER40", "UK100"]:
                return RegimeAlignment.STRONGLY_SUPPORTIVE
            else:
                return RegimeAlignment.SUPPORTIVE

        elif regime == MarketRegime.RISK_OFF:
            if asset in ["XAUUSD", "XAGUSD", "USDJPY", "USDCHF"]:
                return RegimeAlignment.SUPPORTIVE
            elif asset in ["US500", "US100", "US30"]:
                return RegimeAlignment.NEGATIVE
            else:
                return RegimeAlignment.NEUTRAL

        elif regime == MarketRegime.TRENDING:
            return RegimeAlignment.SUPPORTIVE

        elif regime == MarketRegime.RANGING:
            return RegimeAlignment.NEUTRAL

        elif regime == MarketRegime.TRANSITION:
            return RegimeAlignment.MIXED

        elif regime == MarketRegime.VOLATILE:
            if asset in ["XAUUSD", "XAGUSD"]:
                return RegimeAlignment.SUPPORTIVE
            else:
                return RegimeAlignment.NEGATIVE

        return RegimeAlignment.NEUTRAL

    def _calculate_asset_score(
        self, asset: str, dimensions: dict[str, MarketDimension]
    ) -> float:
        relevant_scores = []

        if asset in ["US500", "US100", "US30", "GER40", "UK100"]:
            for dim in ["risk_sentiment", "macro_growth", "liquidity"]:
                if dim in dimensions:
                    relevant_scores.append(dimensions[dim].value)
        elif asset in ["XAUUSD", "XAGUSD"]:
            for dim in ["inflation_pressure", "volatility"]:
                if dim in dimensions:
                    relevant_scores.append(dimensions[dim].value)
            if "risk_sentiment" in dimensions:
                relevant_scores.append(100 - dimensions["risk_sentiment"].value)
        elif asset in ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD"]:
            for dim in ["macro_growth", "risk_sentiment"]:
                if dim in dimensions:
                    relevant_scores.append(dimensions[dim].value)
        elif asset in ["USDJPY", "USDCHF"]:
            if "risk_sentiment" in dimensions:
                relevant_scores.append(100 - dimensions["risk_sentiment"].value)
        else:
            if "risk_sentiment" in dimensions:
                relevant_scores.append(dimensions["risk_sentiment"].value)

        if relevant_scores:
            return sum(relevant_scores) / len(relevant_scores)
        return 50

    def _determine_primary_factor(
        self, asset: str, dimensions: dict[str, MarketDimension]
    ) -> str:
        factors = {
            "EURUSD": "Rate Differential",
            "GBPUSD": "Rate Differential",
            "USDJPY": "Yield Differential",
            "AUDUSD": "Commodity Prices",
            "NZDUSD": "Commodity Prices",
            "USDCAD": "Oil Prices",
            "USDCHF": "Safe Haven Flows",
            "XAUUSD": "Real Yields",
            "XAGUSD": "Industrial Demand",
            "US500": "Growth + Earnings",
            "US100": "Tech Sentiment",
            "US30": "Economic Growth",
            "GER40": "European Growth",
            "UK100": "Energy Prices",
            "JP225": "Global Growth",
            "HK50": "China Growth",
            "AU200": "Commodity Prices",
        }
        return factors.get(asset, "Market Sentiment")

    def _calculate_asset_confidence(
        self, asset: str, normalized_data: dict[str, Any]
    ) -> float:
        price_data = normalized_data.get("price", {})
        symbols = price_data.get("symbols", {})
        if asset in symbols:
            return 85.0
        return 60.0

    def _determine_freshness(self, normalized_data: dict[str, Any]) -> str:
        return "LIVE"
