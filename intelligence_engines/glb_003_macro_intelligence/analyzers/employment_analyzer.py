# -*- coding: utf-8 -*-
"""Employment Analyzer for Macro Intelligence Engine"""

from typing import Dict, Any, List


class EmploymentAnalyzer:
    """Analyzes employment data"""

    def analyze(self, emp_data: List[Dict]) -> Dict[str, Any]:
        """Analyze employment data and return insights"""
        if not emp_data:
            return {
                "growth": 0.0,
                "trend": "unknown",
                "confidence": 0.0,
                "score": 50.0,
                "period": "current",
            }

        latest = emp_data[-1]
        previous = emp_data[-2] if len(emp_data) > 1 else None

        growth = latest.get("value", 0.0)
        growth_change = 0.0

        if previous:
            growth_change = growth - previous.get("value", 0.0)

        if growth_change > 0.1:
            trend = "improving"
        elif growth_change < -0.1:
            trend = "worsening"
        else:
            trend = "stable"

        # Score: 0.5% growth = 50, 1%+ = 100, -0.5% = 0
        score = 50 + (growth * 50)
        score = max(0, min(100, score))

        confidence = 65.0
        if len(emp_data) > 4:
            confidence += 10.0

        return {
            "growth": growth,
            "growth_change": growth_change,
            "trend": trend,
            "confidence": min(confidence, 90.0),
            "score": score,
            "period": latest.get("period", "current"),
            "country": latest.get("country", "US"),
        }
