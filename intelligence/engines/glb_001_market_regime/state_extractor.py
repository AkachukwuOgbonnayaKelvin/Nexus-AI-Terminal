"""
GLB-001 Market Regime Engine - State Extractor
"""

import logging
from typing import Any

from .constants import DIMENSION_WEIGHTS
from .schemas import MarketDimension

logger = logging.getLogger(__name__)


class StateExtractor:
    """Extracts market state from normalized input data."""

    def __init__(self):
        self.dimensions: dict[str, MarketDimension] = {}

    def extract(self, normalized_data: dict[str, Any]) -> dict[str, MarketDimension]:
        """Extract all market dimensions from normalized data."""
        self.dimensions = {}

        self.dimensions["risk_sentiment"] = self._extract_risk_sentiment(
            normalized_data
        )
        self.dimensions["trend_strength"] = self._extract_trend_strength(
            normalized_data
        )
        self.dimensions["volatility"] = self._extract_volatility(normalized_data)
        self.dimensions["momentum"] = self._extract_momentum(normalized_data)
        self.dimensions["breadth"] = self._extract_breadth(normalized_data)
        self.dimensions["macro_growth"] = self._extract_macro_growth(normalized_data)
        self.dimensions["inflation_pressure"] = self._extract_inflation(normalized_data)
        self.dimensions["liquidity"] = self._extract_liquidity(normalized_data)

        return self.dimensions

    def _extract_risk_sentiment(self, data: dict[str, Any]) -> MarketDimension:
        risk = data.get("risk", {})
        sentiment_score = risk.get("risk_sentiment", 50)
        return MarketDimension(
            name="risk_sentiment",
            value=sentiment_score,
            weight=DIMENSION_WEIGHTS["risk_sentiment"],
            contribution=sentiment_score * DIMENSION_WEIGHTS["risk_sentiment"],
            direction="BULLISH"
            if sentiment_score > 60
            else "BEARISH"
            if sentiment_score < 40
            else "NEUTRAL",
        )

    def _extract_trend_strength(self, data: dict[str, Any]) -> MarketDimension:
        trend = data.get("trend", {})
        strength = trend.get("trend_strength", 50)
        return MarketDimension(
            name="trend_strength",
            value=strength,
            weight=DIMENSION_WEIGHTS["trend_strength"],
            contribution=strength * DIMENSION_WEIGHTS["trend_strength"],
            direction="BULLISH"
            if strength > 60
            else "BEARISH"
            if strength < 40
            else "NEUTRAL",
        )

    def _extract_volatility(self, data: dict[str, Any]) -> MarketDimension:
        vol = data.get("volatility", {})
        vix = vol.get("vix", 20)
        if vix <= 10:
            score = 100
        elif vix >= 40:
            score = 0
        else:
            score = 100 - ((vix - 10) / 30 * 100)
        return MarketDimension(
            name="volatility",
            value=score,
            weight=DIMENSION_WEIGHTS["volatility"],
            contribution=score * DIMENSION_WEIGHTS["volatility"],
            direction="BULLISH"
            if score > 70
            else "BEARISH"
            if score < 40
            else "NEUTRAL",
        )

    def _extract_momentum(self, data: dict[str, Any]) -> MarketDimension:
        momentum_score = 50
        price = data.get("price", {})
        symbols = price.get("symbols", {})
        if "US500" in symbols:
            change = symbols["US500"].get("change_20d", 0)
            momentum_score = 50 + (change * 5)
            momentum_score = max(0, min(100, momentum_score))
        return MarketDimension(
            name="momentum",
            value=momentum_score,
            weight=DIMENSION_WEIGHTS["momentum"],
            contribution=momentum_score * DIMENSION_WEIGHTS["momentum"],
            direction="BULLISH"
            if momentum_score > 60
            else "BEARISH"
            if momentum_score < 40
            else "NEUTRAL",
        )

    def _extract_breadth(self, data: dict[str, Any]) -> MarketDimension:
        breadth = data.get("breadth", {})
        ratio = breadth.get("breadth_ratio", 1.0)
        breadth_score = 50 + ((ratio - 1.0) * 50)
        breadth_score = max(0, min(100, breadth_score))
        return MarketDimension(
            name="breadth",
            value=breadth_score,
            weight=DIMENSION_WEIGHTS["breadth"],
            contribution=breadth_score * DIMENSION_WEIGHTS["breadth"],
            direction="BULLISH"
            if breadth_score > 60
            else "BEARISH"
            if breadth_score < 40
            else "NEUTRAL",
        )

    def _extract_macro_growth(self, data: dict[str, Any]) -> MarketDimension:
        macro = data.get("macro", {})
        growth = macro.get("growth", {})
        if "score" in growth:
            growth_score = growth.get("score", 50)
        else:
            gdp = growth.get("gdp", {}).get("value", 2.0)
            growth_score = gdp * 25
            growth_score = max(0, min(100, growth_score))
        return MarketDimension(
            name="macro_growth",
            value=growth_score,
            weight=DIMENSION_WEIGHTS["macro_growth"],
            contribution=growth_score * DIMENSION_WEIGHTS["macro_growth"],
            direction="BULLISH"
            if growth_score > 60
            else "BEARISH"
            if growth_score < 40
            else "NEUTRAL",
        )

    def _extract_inflation(self, data: dict[str, Any]) -> MarketDimension:
        macro = data.get("macro", {})
        inflation = macro.get("inflation", {})
        if "score" in inflation:
            score = inflation.get("score", 50)
            if score <= 20:
                inflation_score = 100
            elif score <= 40:
                inflation_score = 75
            elif score <= 60:
                inflation_score = 50
            elif score <= 80:
                inflation_score = 25
            else:
                inflation_score = 0
        else:
            inflation_score = 50
        return MarketDimension(
            name="inflation_pressure",
            value=inflation_score,
            weight=DIMENSION_WEIGHTS["inflation_pressure"],
            contribution=inflation_score * DIMENSION_WEIGHTS["inflation_pressure"],
            direction="BULLISH"
            if inflation_score > 60
            else "BEARISH"
            if inflation_score < 40
            else "NEUTRAL",
        )

    def _extract_liquidity(self, data: dict[str, Any]) -> MarketDimension:
        risk = data.get("risk", {})
        liquidity_score = risk.get("risk_on_score", 50)
        return MarketDimension(
            name="liquidity",
            value=liquidity_score,
            weight=DIMENSION_WEIGHTS["liquidity"],
            contribution=liquidity_score * DIMENSION_WEIGHTS["liquidity"],
            direction="BULLISH"
            if liquidity_score > 60
            else "BEARISH"
            if liquidity_score < 40
            else "NEUTRAL",
        )
