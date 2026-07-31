import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.asset_macro_intelligence.macro_engine import MacroIntelligenceEngine

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = MacroIntelligenceEngine()
    engine.run()
