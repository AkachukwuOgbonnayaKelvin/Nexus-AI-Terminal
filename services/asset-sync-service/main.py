"""
Asset Synchronizer Service Entry Point
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sync_prices import PriceSynchronizer

if __name__ == "__main__":
    synchronizer = PriceSynchronizer()
    synchronizer.run_continuous()
