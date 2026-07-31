"""
Asset Synchronizer Service Entry Point
"""
import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.asset_sync_service.sync_prices import PriceSynchronizer

if __name__ == "__main__":
    synchronizer = PriceSynchronizer()
    synchronizer.run_continuous()
