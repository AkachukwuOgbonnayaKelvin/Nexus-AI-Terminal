import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.asset_monetary_engine.monetary_engine import MonetaryEngine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = MonetaryEngine()
    engine.run()
