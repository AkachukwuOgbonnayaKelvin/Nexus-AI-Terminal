"""
GLB-007 Capital Flows & Liquidity Intelligence Engine

Analyzes capital flows and liquidity conditions and produces:
1. Core Intelligence: Flow and liquidity analysis
2. Asset Impact Matrix: How flows and liquidity affect assets
"""

from .engine import CapitalFlowsEngine

__all__ = [
    "CapitalFlowsEngine",
]
