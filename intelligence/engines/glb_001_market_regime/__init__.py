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

from .engine import MarketRegimeEngine
from .schemas import (
    RegimeReport,
    RegimeSignal,
    RegimeEvidence,
    RegimeRisk,
    RegimeDriver,
)
from .constants import MarketRegime, TransitionState, RegimeAlignment

__all__ = [
    "MarketRegimeEngine",
    "RegimeReport",
    "RegimeSignal",
    "RegimeEvidence",
    "RegimeRisk",
    "RegimeDriver",
    "MarketRegime",
    "TransitionState",
    "RegimeAlignment",
]
