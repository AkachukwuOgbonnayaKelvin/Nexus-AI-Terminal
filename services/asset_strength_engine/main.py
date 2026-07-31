import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.asset_strength_engine.strength_engine import CurrencyStrengthEngine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = CurrencyStrengthEngine()
    engine.run()
