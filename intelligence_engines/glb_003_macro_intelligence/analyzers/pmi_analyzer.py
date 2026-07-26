"""PMI Analyzer for Macro Intelligence Engine"""

from typing import Any


class PMIAnalyzer:
    """Analyzes PMI data"""

    def analyze(self, pmi_data: list[dict]) -> dict[str, Any]:
        """Analyze PMI data and return insights"""
        if not pmi_data:
            return {
                "value": 50.0,
                "trend": "unknown",
                "confidence": 0.0,
                "score": 50.0,
                "period": "current",
            }

        latest = pmi_data[-1]
        previous = pmi_data[-2] if len(pmi_data) > 1 else None

        value = latest.get("value", 50.0)
        value_change = 0.0

        if previous:
            value_change = value - previous.get("value", 50.0)

        if value_change > 1.0:
            trend = "improving"
        elif value_change < -1.0:
            trend = "deteriorating"
        else:
            trend = "stable"

        # Score: 50 = 50, 60+ = 100, 40- = 0
        score = 50 + ((value - 50) * 2.5)
        score = max(0, min(100, score))

        confidence = 65.0
        if len(pmi_data) > 4:
            confidence += 10.0

        return {
            "value": value,
            "value_change": value_change,
            "trend": trend,
            "confidence": min(confidence, 90.0),
            "score": score,
            "period": latest.get("period", "current"),
            "country": latest.get("country", "US"),
            "interpretation": self._interpret_pmi(value),
        }

    def _interpret_pmi(self, value: float) -> str:
        """Interpret PMI value"""
        if value > 55:
            return "Strong expansion"
        elif value > 52:
            return "Moderate expansion"
        elif value > 50:
            return "Slight expansion"
        elif value > 48:
            return "Slight contraction"
        elif value > 45:
            return "Moderate contraction"
        else:
            return "Strong contraction"
