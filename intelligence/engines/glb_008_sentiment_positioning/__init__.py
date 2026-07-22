"""
GLB-008 Sentiment & Positioning Intelligence Engine

Analyzes sentiment and positioning and produces:
1. Core Intelligence: Sentiment and positioning analysis
2. Asset Impact Matrix: How sentiment affects assets
"""

from .engine import SentimentPositioningEngine

__all__ = [
    "SentimentPositioningEngine",
]
