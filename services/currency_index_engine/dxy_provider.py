import math
from services.currency_index_engine.baskets import DXY_WEIGHTS, DXY_CONSTANT

class DXYProvider:
    @staticmethod
    def calculate_dxy(pair_prices: dict) -> float:
        """
        pair_prices: dict of symbol -> latest close price
        Returns DXY value (fallback calculation).
        """
        product = 1.0
        for symbol, weight in DXY_WEIGHTS.items():
            price = pair_prices.get(symbol)
            if price is None:
                return None
            product *= price ** weight
        return DXY_CONSTANT * product
