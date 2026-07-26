"""
GLB-001 Market Regime Engine - Input Normalizer
"""

import logging
from datetime import datetime
from typing import Any

from .constants import NDIP_TOPICS

logger = logging.getLogger(__name__)


class InputNormalizer:
    """
    Consumes NDIP contracts and normalizes them for GLB-001.
    Does NOT query raw warehouse or other engines directly.
    """

    def __init__(self):
        self.last_consumed_at: datetime | None = None
        self.input_data: dict[str, Any] = {}

    def consume_ndip(self, topic: str, payload: dict[str, Any]) -> None:
        """Consume NDIP contract payload."""
        self.last_consumed_at = datetime.utcnow()
        self.input_data[topic] = payload
        logger.debug(f"Consumed NDIP topic: {topic}")

    def normalize(self) -> dict[str, Any]:
        """Normalize all consumed data into a unified structure."""
        return {
            "price": self._normalize_price(),
            "trend": self._normalize_trend(),
            "volatility": self._normalize_volatility(),
            "breadth": self._normalize_breadth(),
            "risk": self._normalize_risk(),
            "macro": self._normalize_macro(),
        }

    def _normalize_price(self) -> dict[str, Any]:
        price_data = self.input_data.get(NDIP_TOPICS["PRICE_SNAPSHOT"], {})
        return {
            "symbols": price_data.get("symbols", {}),
            "timestamp": price_data.get("timestamp"),
        }

    def _normalize_trend(self) -> dict[str, Any]:
        trend_data = self.input_data.get(NDIP_TOPICS["TREND_SNAPSHOT"], {})
        return {
            "trend_direction": trend_data.get("direction"),
            "trend_strength": trend_data.get("strength", 0),
            "trend_duration": trend_data.get("duration"),
        }

    def _normalize_volatility(self) -> dict[str, Any]:
        vol_data = self.input_data.get(NDIP_TOPICS["VOLATILITY_SNAPSHOT"], {})
        return {
            "vix": vol_data.get("vix", 20),
            "atr": vol_data.get("atr", 0),
            "std_dev": vol_data.get("std_dev", 0),
            "volatility_rank": vol_data.get("rank", 0),
        }

    def _normalize_breadth(self) -> dict[str, Any]:
        breadth_data = self.input_data.get(NDIP_TOPICS["BREADTH_SNAPSHOT"], {})
        return {
            "advancers": breadth_data.get("advancers", 0),
            "decliners": breadth_data.get("decliners", 0),
            "new_highs": breadth_data.get("new_highs", 0),
            "new_lows": breadth_data.get("new_lows", 0),
            "breadth_ratio": breadth_data.get("ratio", 1.0),
        }

    def _normalize_risk(self) -> dict[str, Any]:
        risk_data = self.input_data.get(NDIP_TOPICS["RISK_SNAPSHOT"], {})
        return {
            "risk_sentiment": risk_data.get("sentiment", 50),
            "risk_on_score": risk_data.get("risk_on_score", 50),
            "risk_off_score": risk_data.get("risk_off_score", 50),
        }

    def _normalize_macro(self) -> dict[str, Any]:
        macro_data = self.input_data.get(NDIP_TOPICS["MACRO_CONDITIONS"], {})
        return {
            "growth": macro_data.get("growth", {}),
            "inflation": macro_data.get("inflation", {}),
            "employment": macro_data.get("employment", {}),
            "pmi": macro_data.get("pmi", {}),
        }

    def is_fresh(self, max_age_seconds: int = 300) -> bool:
        """Check if input data is fresh."""
        if self.last_consumed_at is None:
            return False
        age = (datetime.utcnow() - self.last_consumed_at).total_seconds()
        return age < max_age_seconds

    def has_required_data(self) -> bool:
        """Check if all required NDIP topics are available."""
        required_topics = [
            NDIP_TOPICS["PRICE_SNAPSHOT"],
            NDIP_TOPICS["TREND_SNAPSHOT"],
            NDIP_TOPICS["VOLATILITY_SNAPSHOT"],
        ]
        return all(topic in self.input_data for topic in required_topics)
