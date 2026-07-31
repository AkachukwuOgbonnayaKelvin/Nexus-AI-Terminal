import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.asset_intermarket_engine.intermarket_engine import IntermarketEngine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = IntermarketEngine()
    engine.run()
