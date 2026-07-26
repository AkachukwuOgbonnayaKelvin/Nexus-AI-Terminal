"""
GLB-009 Market Memory & Historical Analogy Intelligence Engine - Cross-Asset Confirmation
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class CrossAssetConfirmation:
    """Analyze cross-asset confirmation of historical analogues"""

    def __init__(self):
        self.asset_groups = {
            "safe_havens": ["XAUUSD", "USDCHF", "USDJPY"],
            "risk_assets": ["US500", "US100", "AUDUSD", "NZDUSD"],
            "commodities": ["WTI", "BRENT", "XAGUSD"],
            "bonds": ["US10Y", "US30Y"],
        }

    def analyze_confirmation(
        self, analogues: list[dict], current_environment: dict
    ) -> dict[str, Any]:
        """
        Analyze cross-asset confirmation.

        Returns:
            Dict with cross-asset confirmation analysis
        """
        if not analogues:
            return {
                "status": "NO_DATA",
                "agreement": 0,
                "confirmation_level": "NONE",
                "confidence": 0,
            }

        # Determine current asset directions
        current_directions = self._get_current_directions(current_environment)

        # Determine historical asset directions
        historical_directions = self._get_historical_directions(analogues)

        # Calculate agreement
        agreements = {}
        for asset, current_dir in current_directions.items():
            if asset in historical_directions:
                hist_dir = historical_directions[asset]
                agreements[asset] = current_dir == hist_dir

        # Calculate overall agreement
        if agreements:
            agreement_ratio = sum(1 for v in agreements.values() if v) / len(agreements)
        else:
            agreement_ratio = 0

        # Determine confirmation level
        if agreement_ratio >= 0.8:
            confirmation = "STRONG"
        elif agreement_ratio >= 0.6:
            confirmation = "MODERATE"
        elif agreement_ratio >= 0.4:
            confirmation = "WEAK"
        else:
            confirmation = "CONTRADICTORY"

        return {
            "status": "OPERATIONAL",
            "agreement": agreement_ratio * 100,
            "confirmation_level": confirmation,
            "agreements": agreements,
            "asset_count": len(agreements),
            "confidence": min(95, 60 + agreement_ratio * 30),
        }

    def _get_current_directions(self, environment: dict) -> dict[str, str]:
        """Get current asset directions from environment"""
        directions = {}
        asset_impacts = environment.get("asset_impacts", {})
        for asset, impact in asset_impacts.items():
            if isinstance(impact, dict) and "score" in impact:
                score = impact["score"]
                if score > 10:
                    directions[asset] = "BULLISH"
                elif score < -10:
                    directions[asset] = "BEARISH"
                else:
                    directions[asset] = "NEUTRAL"
        return directions

    def _get_historical_directions(self, analogues: list[dict]) -> dict[str, str]:
        """Get historical asset directions from analogues"""
        directions = {}
        asset_returns = {}

        for analogue in analogues:
            window = analogue.get("window")
            if not window:
                continue

            # Get assets from the window
            if hasattr(window, "assets") and window.assets:
                for asset, asset_data in window.assets.items():
                    if (
                        hasattr(asset_data, "forward_returns")
                        and asset_data.forward_returns
                    ):
                        # Check if we can get a return for this asset
                        for key, fr in asset_data.forward_returns.items():
                            if hasattr(fr, "return_pct") and fr.return_pct != 0:
                                if asset not in asset_returns:
                                    asset_returns[asset] = []
                                asset_returns[asset].append(fr.return_pct)
                                break

        # Calculate average return per asset
        for asset, returns in asset_returns.items():
            if returns:
                avg_return = sum(returns) / len(returns)
                if avg_return > 0.1:
                    directions[asset] = "BULLISH"
                elif avg_return < -0.1:
                    directions[asset] = "BEARISH"
                else:
                    directions[asset] = "NEUTRAL"

        return directions
