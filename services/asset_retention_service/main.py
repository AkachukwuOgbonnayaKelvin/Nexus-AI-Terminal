"""
Entry point for Retention Manager.
"""
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.asset_retention_service.retention_manager import RetentionManager

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = RetentionManager()
    manager.run_retention()
