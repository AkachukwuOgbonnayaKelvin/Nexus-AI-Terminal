"""
Test the synchronizer with a single sync cycle
"""
from sync_prices import PriceSynchronizer

def test_sync():
    print("Ì¥ß Testing Price Synchronizer...")
    sync = PriceSynchronizer()
    try:
        sync.connect()
        count = sync.sync_once()
        print(f"‚úÖ Test complete. Synced {count} records.")
    except Exception as e:
        print(f"‚ùå Test failed: {e}")
    finally:
        if sync.core_conn:
            sync.core_conn.close()
        if sync.asset_conn:
            sync.asset_conn.close()

if __name__ == "__main__":
    test_sync()
