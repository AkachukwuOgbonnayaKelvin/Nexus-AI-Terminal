# -*- coding: utf-8 -*-
"""GDP Analyzer for Macro Intelligence Engine"""

from typing import Dict, Any, List


class GDPAnalyzer:
    """Analyzes GDP data"""

    def analyze(self, gdp_data: List[Dict]) -> Dict[str, Any]:
        """Analyze GDP data and return insights"""
        if not gdp_data:
            return {
                "growth": 0.0,
                "trend": "unknown",
                "confidence": 0.0,
                "score": 50.0,
                "period": "current",
            }

        # Get latest GDP data
        latest = gdp_data[-1]
        previous = gdp_data[-2] if len(gdp_data) > 1 else None

        growth = latest.get("value", 0.0)
        growth_change = 0.0

        if previous:
            growth_change = growth - previous.get("value", 0.0)

        # Determine trend
        if growth_change > 0.3:
            trend = "accelerating"
        elif growth_change < -0.3:
            trend = "decelerating"
        else:
            trend = "stable"

        # Calculate score (GDP growth converted to 0-100 scale)
        # 0% growth = 50, 3%+ growth = 100, -2% growth = 0
        score = 50 + (growth * 10)
        score = max(0, min(100, score))

        # Confidence based on data quality and consistency
        confidence = 70.0
        if len(gdp_data) > 4:
            confidence += 10.0
        if previous:
            confidence += 5.0

        return {
            "growth": growth,
            "growth_change": growth_change,
            "trend": trend,
            "confidence": min(confidence, 95.0),
            "score": score,
            "period": latest.get("period", "current"),
            "country": latest.get("country", "US"),
        }
