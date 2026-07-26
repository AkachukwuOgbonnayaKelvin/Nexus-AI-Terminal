"""
GLB-008 Sentiment & Positioning Intelligence Engine - Sentiment Analyzer
"""

import logging
from typing import Any

from ..constants import SentimentState
from ..input.schemas import OptionsSentimentInput, RetailSentimentInput

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Analyze market sentiment"""

    def analyze_sentiment(
        self,
        retail_data: list[RetailSentimentInput],
        options_data: list[OptionsSentimentInput],
    ) -> dict[str, Any]:
        """
        Analyze sentiment from retail and options data.

        Returns:
            Dict with sentiment analysis
        """
        sentiment_scores = []

        # Analyze retail sentiment
        if retail_data:
            retail_scores = [d.net_sentiment for d in retail_data]
            avg_retail = sum(retail_scores) / len(retail_scores) if retail_scores else 0
            sentiment_scores.append(avg_retail * 0.3)

        # Analyze options sentiment
        if options_data:
            option_scores = []
            for opt in options_data:
                # Lower put/call = bullish sentiment
                option_score = (1 - opt.put_call_ratio) * 50
                option_scores.append(option_score)

            avg_option = sum(option_scores) / len(option_scores) if option_scores else 0
            sentiment_scores.append(avg_option * 0.3)

        # Calculate overall sentiment
        if not sentiment_scores:
            return {
                "status": "NO_DATA",
                "sentiment_score": 50.0,
                "sentiment_state": SentimentState.NEUTRAL.value,
                "confidence": 0.0,
            }

        overall_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        overall_sentiment = max(0, min(100, overall_sentiment))

        # Determine state
        if overall_sentiment > 75:
            state = SentimentState.RISK_ON.value
        elif overall_sentiment < 25:
            state = SentimentState.RISK_OFF.value
        elif overall_sentiment > 60:
            state = SentimentState.RISK_ON.value
        elif overall_sentiment < 40:
            state = SentimentState.RISK_OFF.value
        else:
            state = SentimentState.NEUTRAL.value

        # Calculate confidence
        confidence = 60.0
        if retail_data:
            confidence += 10
        if options_data:
            confidence += 10
        confidence = min(95, confidence)

        return {
            "status": "OPERATIONAL",
            "sentiment_score": overall_sentiment,
            "sentiment_state": state,
            "retail_count": len(retail_data),
            "options_count": len(options_data),
            "confidence": confidence,
        }
