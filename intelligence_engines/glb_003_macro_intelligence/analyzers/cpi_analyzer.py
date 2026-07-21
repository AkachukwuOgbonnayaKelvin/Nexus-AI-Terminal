# -*- coding: utf-8 -*-
"""CPI Analyzer for Macro Intelligence Engine"""

from typing import Dict, Any, List


class CPIAnalyzer:
    """Analyzes CPI data"""

    def analyze(self, cpi_data: List[Dict]) -> Dict[str, Any]:
        """Analyze CPI data and return insights"""
        if not cpi_data:
            return {
                "rate": 0.0,
                "trend": "unknown",
                "confidence": 0.0,
                "score": 50.0,
                "period": "current",
            }

        # Get latest CPI data
        latest = cpi_data[-1]
        previous = cpi_data[-2] if len(cpi_data) > 1 else None

        rate = latest.get("value", 0.0)
        rate_change = 0.0

        if previous:
            rate_change = rate - previous.get("value", 0.0)

        # Determine trend
        if rate_change > 0.2:
            trend = "rising"
        elif rate_change < -0.2:
            trend = "falling"
        else:
            trend = "stable"

        # Calculate score (inflation rate converted to 0-100 scale)
        # 2.5% inflation = 50, 0% = 100, 5%+ = 0
        score = 100 - (rate * 15)
        score = max(0, min(100, score))

        confidence = 70.0
        if len(cpi_data) > 4:
            confidence += 10.0
        if previous:
            confidence += 5.0

        return {
            "rate": rate,
            "rate_change": rate_change,
            "trend": trend,
            "confidence": min(confidence, 95.0),
            "score": score,
            "period": latest.get("period", "current"),
            "country": latest.get("country", "US"),
        }
