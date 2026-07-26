"""Metrics collection for ECO-002"""


class EarningsMetrics:
    def collect(self):
        return {
            "symbols_collected": 0,
            "earnings_count": 0,
            "error_rate": 0,
            "last_success": None,
        }
