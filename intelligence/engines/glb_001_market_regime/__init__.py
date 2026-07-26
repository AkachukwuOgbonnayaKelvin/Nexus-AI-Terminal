"""
GLB-001 Market Regime Engine

Classifies global market environment into regimes:
- RISK_ON / RISK_OFF
- TRENDING / RANGING
- TRANSITION / VOLATILE

Consumes NDIP contracts from:
- MKT-001 (Market Price)
- GLB-003 (Macro Intelligence)

Produces Universal EngineReport format.
"""

from .constants import MarketRegime, RegimeAlignment, TransitionState
from .engine import MarketRegimeEngine
from .schemas import (
    RegimeDriver,
    RegimeEvidence,
    RegimeReport,
    RegimeRisk,
    RegimeSignal,
)

__all__ = [
    "MarketRegime",
    "MarketRegimeEngine",
    "RegimeAlignment",
    "RegimeDriver",
    "RegimeEvidence",
    "RegimeReport",
    "RegimeRisk",
    "RegimeSignal",
    "TransitionState",
]
