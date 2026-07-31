import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.asset_preparation_service.preparation_manager import PreparationManager

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = PreparationManager()
    manager.run()
