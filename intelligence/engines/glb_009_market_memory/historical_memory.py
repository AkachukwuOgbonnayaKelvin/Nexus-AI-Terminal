"""
GLB-009: Market Memory Intelligence Engine

Compares current market state with historical analogues
to identify similar periods and predict outcomes.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import numpy as np

from intelligence.engines.base import BaseEngine
from intelligence.engines.schemas import NormalizedOutput

logger = logging.getLogger(__name__)


class HistoricalMemory(BaseEngine):
    """
    Market Memory Engine - GLB-009.

    Compares current market conditions with historical windows
    to find analogues and predict forward outcomes.
    """

    ENGINE_ID = "GLB-009"
    ENGINE_NAME = "Market Memory Intelligence"

    def __init__(self):
        super().__init__()
        self.historical_windows: list[dict] = []
        self.analogues: list[dict] = []
        self._load_historical_data()

    def _load_historical_data(self) -> None:
        """Load historical windows from JSON files."""
        try:
            # Try multiple possible locations
            possible_paths = [
                Path("historical_windows_glb009.json"),
                Path("canonical_historical_windows.json"),
                Path("data/historical_windows.json"),
                Path("../historical_windows_glb009.json"),
            ]

            for path in possible_paths:
                if path.exists():
                    with open(path, "r") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self.historical_windows = data
                            logger.info(
                                f"Loaded {len(data)} historical windows from {path}"
                            )
                            return
                        elif isinstance(data, dict) and "windows" in data:
                            self.historical_windows = data["windows"]
                            logger.info(
                                f"Loaded {len(self.historical_windows)} historical windows from {path}"
                            )
                            return

            logger.warning("No historical data found. Using empty windows.")

        except Exception as e:
            logger.error(f"Failed to load historical data: {e}")
            self.historical_windows = []

    def process(self, **kwargs) -> NormalizedOutput:
        """
        Process current market data and find historical analogues.
        """
        try:
            current_state = kwargs.get("current_state", {})
            asset = kwargs.get("asset", "USD")

            # Find analogues
            analogues = self.find_analogues(current_state)

            # Calculate forward bias
            forward_bias = self.calculate_forward_bias(analogues, asset)

            return NormalizedOutput(
                engine_id=self.ENGINE_ID,
                domain="MARKET_MEMORY",
                entity=asset,
                score=forward_bias.get("score", 0.0),
                direction=forward_bias.get("direction", "NEUTRAL"),
                confidence=forward_bias.get("confidence", 50.0),
                reliability=0.85,
                freshness=0.9,
                evidence_quality=0.8,
                drivers=forward_bias.get("drivers", []),
                risks=forward_bias.get("risks", []),
                evidence=[],
                source_data={
                    "analogues_found": len(analogues),
                    "best_match": analogues[0] if analogues else None,
                    "historical_bias": forward_bias,
                },
                timestamp=datetime.utcnow(),
            )

        except Exception as e:
            logger.error(f"GLB-009 processing error: {e}")
            return self._error_output(str(e))

    def find_analogues(self, current_state: dict) -> list[dict]:
        """
        Find historical windows similar to current state.
        """
        if not self.historical_windows or not current_state:
            return []

        analogues = []

        for window in self.historical_windows:
            similarity = self._calculate_similarity(current_state, window)
            if similarity > 0.5:
                analogues.append(
                    {
                        "window_id": window.get("window_id"),
                        "date": window.get("date"),
                        "similarity": similarity,
                        "regime": window.get("regime"),
                        "forward_outcomes": window.get("forward_outcomes", {}),
                    }
                )

        # Sort by similarity descending
        analogues.sort(key=lambda x: x["similarity"], reverse=True)

        return analogues[:10]

    def calculate_forward_bias(self, analogues: list[dict], asset: str) -> dict:
        """
        Calculate forward bias from analogues.
        """
        if not analogues:
            return {
                "score": 0.0,
                "direction": "NEUTRAL",
                "confidence": 0.0,
                "drivers": [],
                "risks": ["NO_HISTORICAL_ANALOGUES"],
            }

        # Calculate average forward return for the asset
        returns = []
        for a in analogues:
            outcomes = a.get("forward_outcomes", {})
            if asset in outcomes:
                returns.append(outcomes[asset])

        if not returns:
            return {
                "score": 0.0,
                "direction": "NEUTRAL",
                "confidence": 0.0,
                "drivers": [],
                "risks": ["NO_FORWARD_DATA"],
            }

        avg_return = np.mean(returns)
        confidence = min(100, len(analogues) * 10 + 50)

        if avg_return > 2:
            direction = "BULLISH"
        elif avg_return < -2:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"

        return {
            "score": avg_return * 2,  # Scale to -100 to +100
            "direction": direction,
            "confidence": confidence,
            "drivers": ["HISTORICAL_ANALOGUE"],
            "risks": [],
        }

    def _calculate_similarity(self, current: dict, window: dict) -> float:
        """
        Calculate similarity between current state and historical window.
        """
        # Simple similarity based on regime matching
        current_regime = current.get("regime", "UNKNOWN")
        window_regime = window.get("regime", "UNKNOWN")

        if current_regime == window_regime:
            return 0.8
        elif current_regime in ["RISK_ON", "RISK_OFF"] and window_regime in [
            "RISK_ON",
            "RISK_OFF",
        ]:
            return 0.6
        else:
            return 0.3

    def _error_output(self, error_message: str) -> NormalizedOutput:
        """Return error output."""
        return NormalizedOutput(
            engine_id=self.ENGINE_ID,
            domain="MARKET_MEMORY",
            entity="UNKNOWN",
            score=0.0,
            direction="NEUTRAL",
            confidence=0.0,
            reliability=0.0,
            freshness=0.0,
            evidence_quality=0.0,
            drivers=[],
            risks=["ERROR"],
            evidence=[],
            source_data={"error": error_message},
            timestamp=datetime.utcnow(),
        )


# Singleton instance
_historical_memory_instance = None


def get_historical_memory() -> HistoricalMemory:
    """Get singleton HistoricalMemory instance."""
    global _historical_memory_instance
    if _historical_memory_instance is None:
        _historical_memory_instance = HistoricalMemory()
    return _historical_memory_instance
