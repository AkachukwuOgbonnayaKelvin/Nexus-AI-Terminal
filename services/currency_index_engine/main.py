import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.currency_index_engine.engine import CurrencyIndexEngine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = CurrencyIndexEngine()
    engine.run()
