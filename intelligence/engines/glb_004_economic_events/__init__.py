"""
GLB-004 Economic Events Intelligence Engine

Analyzes economic calendar events and produces:
1. Core Intelligence: Event impact analysis
2. Asset Impact Matrix: How events affect assets
"""

from .engine import EconomicEventsEngine

__all__ = [
    "EconomicEventsEngine",
]
