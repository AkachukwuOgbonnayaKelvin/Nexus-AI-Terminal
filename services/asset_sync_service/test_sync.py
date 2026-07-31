"""
Test the synchronizer with a single sync cycle.
"""
import sys
import os

# Add parent directory to path so we can import services
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.asset_sync_service.sync_prices import PriceSynchronizer


def test_sync():
    """Test a single sync cycle."""
    print("Testing Price Synchronizer...")
    sync = PriceSynchronizer()
    try:
        sync.connect()
        count = sync.sync_once()
        print(f"Synced {count} records.")
    except Exception as e:
        print(f"Sync test failed: {e}")
    finally:
        if sync.core_conn:
            sync.core_conn.close()
        if sync.asset_conn:
            sync.asset_conn.close()


if __name__ == "__main__":
    test_sync()
