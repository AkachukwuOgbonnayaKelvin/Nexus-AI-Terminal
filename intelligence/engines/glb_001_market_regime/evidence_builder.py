"""
GLB-001 Market Regime Engine - Evidence Builder
"""

import logging
from typing import Dict, List, Any, Union

from .schemas import RegimeEvidence, MarketDimension

logger = logging.getLogger(__name__)


class EvidenceBuilder:
    """Builds evidence for regime classification."""

    def __init__(self):
        self.direction_resolver = DirectionResolver()

    def build_evidence(
        self, dimensions: Dict[str, MarketDimension], normalized_data: Dict[str, Any]
    ) -> List[RegimeEvidence]:
        """Build evidence list from dimensions and raw data."""
        evidence = []
        evidence.extend(self._build_market_evidence(dimensions, normalized_data))
        evidence.extend(self._build_macro_evidence(dimensions, normalized_data))
        return evidence

    def _build_market_evidence(
        self, dimensions: Dict[str, MarketDimension], data: Dict[str, Any]
    ) -> List[RegimeEvidence]:
        evidence = []

        # 1. Trend Direction
        trend = data.get("trend", {})
        trend_direction = trend.get("trend_direction", "NEUTRAL")
        if trend_direction is None:
            trend_direction = "NEUTRAL"
        evidence.append(
            RegimeEvidence(
                source="MKT-001",
                indicator="trend_direction",
                value=trend_direction,
                contribution=0.85,
                direction=self.direction_resolver.resolve(
                    trend_direction, "trend_direction"
                ),
            )
        )

        # 2. VIX / Volatility
        vol = data.get("volatility", {})
        vix_value = vol.get("vix", 20)
        if vix_value is None:
            vix_value = 20
        vix_direction = (
            "BULLISH" if vix_value < 18 else "BEARISH" if vix_value > 25 else "NEUTRAL"
        )
        evidence.append(
            RegimeEvidence(
                source="MKT-001",
                indicator="vix",
                value=vix_value,
                contribution=0.80,
                direction=vix_direction,
            )
        )

        # 3. Risk Sentiment
        risk = data.get("risk", {})
        risk_sentiment = risk.get("risk_sentiment", 50)
        if risk_sentiment is None:
            risk_sentiment = 50
        risk_direction = (
            "BULLISH"
            if risk_sentiment > 60
            else "BEARISH"
            if risk_sentiment < 40
            else "NEUTRAL"
        )
        evidence.append(
            RegimeEvidence(
                source="MKT-001",
                indicator="risk_sentiment",
                value=risk_sentiment,
                contribution=0.90,
                direction=risk_direction,
            )
        )

        # 4. Market Breadth
        breadth = data.get("breadth", {})
        breadth_ratio = breadth.get("breadth_ratio", 1.0)
        if breadth_ratio is None:
            breadth_ratio = 1.0
        breadth_direction = (
            "BULLISH"
            if breadth_ratio > 1.5
            else "BEARISH"
            if breadth_ratio < 0.7
            else "NEUTRAL"
        )
        evidence.append(
            RegimeEvidence(
                source="MKT-001",
                indicator="breadth_ratio",
                value=breadth_ratio,
                contribution=0.70,
                direction=breadth_direction,
            )
        )

        return evidence

    def _build_macro_evidence(
        self, dimensions: Dict[str, MarketDimension], data: Dict[str, Any]
    ) -> List[RegimeEvidence]:
        evidence = []
        macro = data.get("macro", {})

        # 1. GDP Growth
        growth = macro.get("growth", {})
        growth_score = growth.get("score", 50)
        if growth_score is None:
            growth_score = 50
        growth_direction = (
            "BULLISH"
            if growth_score > 60
            else "BEARISH"
            if growth_score < 40
            else "NEUTRAL"
        )
        evidence.append(
            RegimeEvidence(
                source="GLB-003",
                indicator="gdp_growth",
                value=growth.get("gdp", {}).get("value", 0),
                contribution=0.75,
                direction=growth_direction,
            )
        )

        # 2. Inflation Pressure
        inflation = macro.get("inflation", {})
        inflation_score = inflation.get("score", 50)
        if inflation_score is None:
            inflation_score = 50
        inflation_direction = (
            "BULLISH"
            if inflation_score < 40
            else "BEARISH"
            if inflation_score > 60
            else "NEUTRAL"
        )
        evidence.append(
            RegimeEvidence(
                source="GLB-003",
                indicator="inflation_pressure",
                value=inflation_score,
                contribution=0.70,
                direction=inflation_direction,
            )
        )

        # 3. Employment Growth
        employment = macro.get("employment", {})
        emp_score = employment.get("score", 50)
        if emp_score is None:
            emp_score = 50
        emp_direction = (
            "BULLISH" if emp_score > 60 else "BEARISH" if emp_score < 40 else "NEUTRAL"
        )
        evidence.append(
            RegimeEvidence(
                source="GLB-003",
                indicator="employment_growth",
                value=employment.get("value", 0),
                contribution=0.65,
                direction=emp_direction,
            )
        )

        # 4. PMI
        pmi = macro.get("pmi", {})
        pmi_score = pmi.get("score", 50)
        if pmi_score is None:
            pmi_score = 50
        pmi_direction = (
            "BULLISH" if pmi_score > 55 else "BEARISH" if pmi_score < 45 else "NEUTRAL"
        )
        evidence.append(
            RegimeEvidence(
                source="GLB-003",
                indicator="pmi",
                value=pmi_score,
                contribution=0.60,
                direction=pmi_direction,
            )
        )

        return evidence


class DirectionResolver:
    """
    Centralized direction resolver for evidence.
    Ensures every evidence has a valid direction.
    """

    # Valid direction values
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

    # Mapping for various input states to directions
    STATE_MAP = {
        "BULLISH": BULLISH,
        "EXPANDING": BULLISH,
        "STRONG": BULLISH,
        "LOW_VOLATILITY": BULLISH,
        "RISK_ON": BULLISH,
        "ABOVE": BULLISH,
        "IMPROVING": BULLISH,
        "POSITIVE": BULLISH,
        "GROWING": BULLISH,
        "ACCELERATING": BULLISH,
        "HIGH": BULLISH,
        "BEARISH": BEARISH,
        "CONTRACTING": BEARISH,
        "WEAK": BEARISH,
        "HIGH_VOLATILITY": BEARISH,
        "RISK_OFF": BEARISH,
        "BELOW": BEARISH,
        "DETERIORATING": BEARISH,
        "NEGATIVE": BEARISH,
        "SHRINKING": BEARISH,
        "DECELERATING": BEARISH,
        "LOW": BEARISH,
        "NEUTRAL": NEUTRAL,
        "STABLE": NEUTRAL,
        "MIXED": NEUTRAL,
        "UNKNOWN": NEUTRAL,
        "TRANSITION": NEUTRAL,
        "MODERATE": NEUTRAL,
        "FLAT": NEUTRAL,
    }

    def resolve(self, value: Union[str, float, int, None], indicator: str = "") -> str:
        """
        Resolve a raw value into a standardized direction.

        Returns: "BULLISH", "BEARISH", or "NEUTRAL"
        """
        if value is None:
            logger.warning(
                f"DirectionResolver received None for indicator: {indicator}"
            )
            return self.NEUTRAL

        if isinstance(value, (int, float)):
            return self._resolve_numeric(value, indicator)

        if isinstance(value, str):
            return self._resolve_string(value, indicator)

        logger.warning(
            f"DirectionResolver received unknown type: {type(value)} for indicator: {indicator}"
        )
        return self.NEUTRAL

    def _resolve_numeric(self, value: float, indicator: str) -> str:
        if "vix" in indicator.lower() or "volatility" in indicator.lower():
            if value < 18:
                return self.BULLISH
            elif value > 25:
                return self.BEARISH
            return self.NEUTRAL

        if "pmi" in indicator.lower():
            if value > 55:
                return self.BULLISH
            elif value < 45:
                return self.BEARISH
            return self.NEUTRAL

        if "ratio" in indicator.lower() or "breadth" in indicator.lower():
            if value > 1.5:
                return self.BULLISH
            elif value < 0.7:
                return self.BEARISH
            return self.NEUTRAL

        if value > 60:
            return self.BULLISH
        elif value < 40:
            return self.BEARISH
        return self.NEUTRAL

    def _resolve_string(self, value: str, indicator: str) -> str:
        normalized = value.upper().strip()

        if normalized in self.STATE_MAP:
            return self.STATE_MAP[normalized]

        for key, direction in self.STATE_MAP.items():
            if key in normalized or normalized in key:
                return direction

        logger.warning(
            f"DirectionResolver could not resolve: '{value}' for indicator: {indicator}"
        )
        return self.NEUTRAL
