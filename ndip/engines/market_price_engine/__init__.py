"""Market Price Engine.

Collects price data from multiple sources (MT5, Polygon, Alpha Vantage, etc.)
"""

from .collector import MarketPriceCollector

__all__ = ["MarketPriceCollector"]
