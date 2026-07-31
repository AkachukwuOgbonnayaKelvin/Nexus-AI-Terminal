import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.asset_micro_engine.micro_engine import MicroEngine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = MicroEngine()
    engine.run()
