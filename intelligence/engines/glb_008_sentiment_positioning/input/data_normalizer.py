"""
GLB-008 Sentiment & Positioning Intelligence Engine - Data Normalizer
"""

import logging
from datetime import datetime
from typing import Any

from ..constants import PositioningBias
from .schemas import (
    COTInput,
    InstitutionalPositioningInput,
    OptionsSentimentInput,
    RetailSentimentInput,
)

logger = logging.getLogger(__name__)


class DataNormalizer:
    """Normalize raw NDIP data into canonical format"""

    def normalize_cot(self, raw: dict[str, Any]) -> COTInput | None:
        """Normalize COT data"""
        try:
            return COTInput(
                symbol=raw.get("symbol", "UNKNOWN"),
                report_date=datetime.fromisoformat(
                    raw.get("report_date", datetime.utcnow().isoformat())
                ),
                dealer_long=raw.get("dealer_long", 0.0),
                dealer_short=raw.get("dealer_short", 0.0),
                asset_manager_long=raw.get("asset_manager_long", 0.0),
                asset_manager_short=raw.get("asset_manager_short", 0.0),
                leveraged_funds_long=raw.get("leveraged_funds_long", 0.0),
                leveraged_funds_short=raw.get("leveraged_funds_short", 0.0),
                net_position=raw.get("net_position", 0.0),
                percentile=raw.get("percentile", 50.0),
                confidence=raw.get("confidence", 70.0),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize COT data: {e}")
            return None

    def normalize_retail(self, raw: dict[str, Any]) -> RetailSentimentInput | None:
        """Normalize retail sentiment data"""
        try:
            bullish = raw.get("bullish_percent", 50.0)
            bearish = raw.get("bearish_percent", 50.0)
            return RetailSentimentInput(
                symbol=raw.get("symbol", "UNKNOWN"),
                bullish_percent=bullish,
                bearish_percent=bearish,
                neutral_percent=raw.get("neutral_percent", 0.0),
                net_sentiment=bullish - bearish,
                confidence=raw.get("confidence", 70.0),
                timestamp=datetime.fromisoformat(
                    raw.get("timestamp", datetime.utcnow().isoformat())
                ),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize retail sentiment: {e}")
            return None

    def normalize_institutional(
        self, raw: dict[str, Any]
    ) -> InstitutionalPositioningInput | None:
        """Normalize institutional positioning data"""
        try:
            return InstitutionalPositioningInput(
                asset=raw.get("asset", "UNKNOWN"),
                net_position=raw.get("net_position", 0.0),
                positioning_bias=PositioningBias(
                    raw.get("positioning_bias", "NEUTRAL")
                ),
                percentile=raw.get("percentile", 50.0),
                crowding=raw.get("crowding", 50.0),
                confidence=raw.get("confidence", 70.0),
                timestamp=datetime.fromisoformat(
                    raw.get("timestamp", datetime.utcnow().isoformat())
                ),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize institutional positioning: {e}")
            return None

    def normalize_options(self, raw: dict[str, Any]) -> OptionsSentimentInput | None:
        """Normalize options sentiment data"""
        try:
            return OptionsSentimentInput(
                symbol=raw.get("symbol", "UNKNOWN"),
                put_call_ratio=raw.get("put_call_ratio", 1.0),
                implied_volatility=raw.get("implied_volatility", 20.0),
                skew=raw.get("skew", 0.0),
                sentiment_score=raw.get("sentiment_score", 0.0),
                confidence=raw.get("confidence", 70.0),
                timestamp=datetime.fromisoformat(
                    raw.get("timestamp", datetime.utcnow().isoformat())
                ),
            )
        except Exception as e:
            logger.warning(f"Failed to normalize options sentiment: {e}")
            return None
