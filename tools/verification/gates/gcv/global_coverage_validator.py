"""Global Coverage Validation - Tests earnings data availability by region"""

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from corporate_earnings_engine.collectors.earnings_collector import EarningsCollector


class GlobalCoverageValidator:
    """Validates global earnings coverage by region"""

    def __init__(self):
        self.collector = EarningsCollector()

        # Test symbols by region
        self.regions = {
            "US": {
                "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
                "currency": "USD",
                "min_required": 3,
            },
            "Eurozone": {
                "symbols": ["SAP", "ASML"],
                "currency": "EUR",
                "min_required": 1,
            },
            "UK": {
                "symbols": ["BP.L", "SHEL.L", "HSBA.L"],
                "currency": "GBP",
                "min_required": 1,
            },
            "Japan": {
                "symbols": ["9984.T", "6758.T"],
                "currency": "JPY",
                "min_required": 1,
            },
            "Switzerland": {
                "symbols": ["NESN.SW", "ROG.SW"],
                "currency": "CHF",
                "min_required": 1,
            },
            "Canada": {
                "symbols": ["RY.TO", "TD.TO"],
                "currency": "CAD",
                "min_required": 1,
            },
            "Australia": {
                "symbols": ["BHP.AX", "CBA.AX"],
                "currency": "AUD",
                "min_required": 1,
            },
            "New Zealand": {
                "symbols": ["AIA.NZ", "FPH.NZ"],
                "currency": "NZD",
                "min_required": 1,
            },
        }

    def validate(self) -> dict[str, Any]:
        """Run global coverage validation"""
        results = {
            "name": "GCV",
            "description": "Global Coverage Validation",
            "status": "PENDING",
            "score": 0,
            "checks": [],
            "issues": [],
        }

        passed = 0
        total = 0

        for region, config in self.regions.items():
            total += 1
            check = {
                "name": region,
                "status": "PENDING",
                "message": "",
                "symbols_found": [],
            }

            try:
                observations = self.collector.collect(config["symbols"])

                # Count symbols with data
                symbols_with_data = set()
                for obs in observations:
                    symbols_with_data.add(obs.symbol)

                check["symbols_found"] = list(symbols_with_data)

                if len(symbols_with_data) >= config["min_required"]:
                    check["status"] = "PASS"
                    check["message"] = (
                        f"Found {len(symbols_with_data)} symbols with earnings data"
                    )
                    passed += 1
                elif len(symbols_with_data) > 0:
                    check["status"] = "PARTIAL"
                    check["message"] = (
                        f"Found {len(symbols_with_data)} symbols, need {config['min_required']}"
                    )
                else:
                    check["status"] = "FAIL"
                    check["message"] = f"No earnings data found for {region}"
                    results["issues"].append(
                        {"region": region, "message": check["message"]}
                    )
            except Exception as e:
                check["status"] = "ERROR"
                check["message"] = str(e)
                results["issues"].append({"region": region, "message": str(e)})

            results["checks"].append(check)

        # Calculate score
        results["score"] = int((passed / total) * 100) if total > 0 else 0

        if results["score"] >= 80:
            results["status"] = "PASS"
        elif results["score"] >= 50:
            results["status"] = "PARTIAL"
        else:
            results["status"] = "FAIL"

        return results
