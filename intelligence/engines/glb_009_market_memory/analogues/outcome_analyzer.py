"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Outcome Analyzer
"""

import logging
from statistics import mean, median, stdev
from typing import Any

from ..constants import TimeHorizon

logger = logging.getLogger(__name__)


class OutcomeAnalyzer:
    """Analyze historical outcomes from analogues"""

    def __init__(self):
        self._available_assets = None

    def set_available_assets(self, assets: list[str]) -> None:
        """Set the list of assets available in the historical windows"""
        self._available_assets = assets

    def analyze_outcomes(self, analogues: list[dict], asset: str) -> dict[str, Any]:
        """
        Analyze historical outcomes for a specific asset.
        """
        if not analogues:
            return {
                "status": "NO_DATA",
                "confidence": 0,
                "overall_direction": "NEUTRAL",
                "outcome_distribution": {"BULLISH": 0, "BEARISH": 0, "NEUTRAL": 0},
            }

        if self._available_assets and asset not in self._available_assets:
            return {
                "status": "ASSET_NOT_AVAILABLE",
                "confidence": 0,
                "overall_direction": "NEUTRAL",
                "outcome_distribution": {"BULLISH": 0, "BEARISH": 0, "NEUTRAL": 0},
                "reason": f"Asset {asset} not available",
            }

        # Define horizon keys
        horizon_keys = {
            TimeHorizon.SHORT_TERM: ["1D", "3D"],
            TimeHorizon.MEDIUM_TERM: ["5D", "10D"],
        }

        results = {}
        all_returns = []

        for horizon, keys in horizon_keys.items():
            horizon_returns = []

            for analogue in analogues:
                window = analogue.get("window")
                if not window:
                    continue

                # Get assets from window
                if hasattr(window, "assets") and window.assets:
                    if asset in window.assets:
                        asset_data = window.assets[asset]

                        # Check for forward_returns
                        if (
                            hasattr(asset_data, "forward_returns")
                            and asset_data.forward_returns
                        ):
                            fr_data = asset_data.forward_returns
                            # Try each key for this horizon
                            for key in keys:
                                if key in fr_data:
                                    fr = fr_data[key]
                                    if hasattr(fr, "return_pct"):
                                        horizon_returns.append(fr.return_pct)
                                        break
                        elif (
                            isinstance(asset_data, dict)
                            and "forward_returns" in asset_data
                        ):
                            fr_data = asset_data["forward_returns"]
                            for key in keys:
                                if key in fr_data:
                                    val = fr_data[key]
                                    if isinstance(val, dict) and "return_pct" in val:
                                        horizon_returns.append(val["return_pct"])
                                    elif isinstance(val, (int, float)):
                                        horizon_returns.append(val)
                                    break

            if horizon_returns:
                results[horizon.value] = self._compute_horizon_stats(horizon_returns)
                all_returns.extend(horizon_returns)
            else:
                results[horizon.value] = {
                    "returns": [],
                    "bullish_percent": 0,
                    "bearish_percent": 0,
                    "median_return": 0,
                    "avg_return": 0,
                    "sample_count": 0,
                    "status": "NO_DATA",
                }

        # Calculate outcome distribution
        bullish = sum(1 for r in all_returns if r > 0.1)
        bearish = sum(1 for r in all_returns if r < -0.1)
        neutral = sum(1 for r in all_returns if -0.1 <= r <= 0.1)
        total = len(all_returns) if all_returns else 1

        distribution = {
            "BULLISH": bullish / total if total > 0 else 0,
            "BEARISH": bearish / total if total > 0 else 0,
            "NEUTRAL": neutral / total if total > 0 else 0,
        }

        if distribution["BULLISH"] > 0.45:
            overall_direction = "BULLISH"
            directional_confidence = distribution["BULLISH"] * 100
        elif distribution["BEARISH"] > 0.45:
            overall_direction = "BEARISH"
            directional_confidence = distribution["BEARISH"] * 100
        else:
            overall_direction = "MIXED"
            directional_confidence = 50.0

        return {
            "status": "OPERATIONAL",
            "horizon_results": results,
            "overall_direction": overall_direction,
            "directional_confidence": directional_confidence,
            "outcome_distribution": distribution,
            "mean_return": mean(all_returns) if all_returns else 0,
            "median_return": median(all_returns) if all_returns else 0,
            "sample_count": len(analogues),
            "confidence": min(95, 50 + len(analogues) * 1.5),
        }

    def _compute_horizon_stats(self, returns: list[float]) -> dict[str, Any]:
        if not returns:
            return {
                "returns": [],
                "bullish_percent": 0,
                "bearish_percent": 0,
                "median_return": 0,
                "avg_return": 0,
                "sample_count": 0,
                "status": "NO_DATA",
            }

        bullish = sum(1 for r in returns if r > 0.1)
        bearish = sum(1 for r in returns if r < -0.1)
        total = len(returns)

        return {
            "returns": returns,
            "bullish_percent": (bullish / total) * 100 if total > 0 else 0,
            "bearish_percent": (bearish / total) * 100 if total > 0 else 0,
            "median_return": median(returns) if returns else 0,
            "avg_return": mean(returns) if returns else 0,
            "std_return": stdev(returns) if len(returns) > 1 else 0,
            "max_return": max(returns) if returns else 0,
            "min_return": min(returns) if returns else 0,
            "sample_count": total,
            "status": "OPERATIONAL",
        }
