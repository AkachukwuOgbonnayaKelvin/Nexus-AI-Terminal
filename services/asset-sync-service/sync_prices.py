"""
Price Synchronizer - Copies data from core.prices to raw.prices
"""
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
import time
import logging
from typing import List, Dict, Any

from config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PriceSynchronizer:
    def __init__(self):
        self.core_conn = None
        self.asset_conn = None
        self.batch_size = config.batch_size
        
    def connect(self):
        """Establish connections to both databases"""
        try:
            # Core database connection (read-only)
            self.core_conn = psycopg2.connect(
                host=config.core_host,
                port=config.core_port,
                dbname=config.core_dbname,
                user=config.core_user,
                password=config.core_password
            )
            self.core_conn.autocommit = True
            logger.info(f"‚úÖ Connected to core database: {config.core_dbname}")
            
            # Asset database connection (write)
            self.asset_conn = psycopg2.connect(
                host=config.asset_host,
                port=config.asset_port,
                dbname=config.asset_dbname,
                user=config.asset_user,
                password=config.asset_password
            )
            self.asset_conn.autocommit = True
            logger.info(f"‚úÖ Connected to asset database: {config.asset_dbname}")
            
        except Exception as e:
            logger.error(f"‚ùå Connection error: {e}")
            raise
    
    def get_last_sync_timestamp(self) -> datetime:
        """Get the last successful sync timestamp"""
        with self.asset_conn.cursor() as cur:
            cur.execute("""
                SELECT last_timestamp 
                FROM raw.sync_state 
                WHERE stream_name = 'prices'
            """)
            result = cur.fetchone()
            if result and result[0]:
                return result[0]
            return datetime(2000, 1, 1)
    
    def update_sync_state(self, last_timestamp: datetime):
        """Update the sync state with the latest timestamp"""
        with self.asset_conn.cursor() as cur:
            cur.execute("""
                UPDATE raw.sync_state 
                SET last_timestamp = %s, updated_at = NOW()
                WHERE stream_name = 'prices'
            """, (last_timestamp,))
    
    def fetch_new_prices(self, since: datetime) -> List[Dict[str, Any]]:
        """Fetch new prices from core database"""
        query = """
            SELECT 
                symbol,
                timeframe,
                timestamp,
                open,
                high,
                low,
                close,
                volume
            FROM prices
            WHERE timestamp > %s
            ORDER BY timestamp ASC
            LIMIT %s
        """
        
        with self.core_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (since, self.batch_size))
            rows = cur.fetchall()
            return rows
    
    def upsert_prices(self, prices: List[Dict[str, Any]]) -> int:
        """Insert or update prices in raw.prices"""
        if not prices:
            return 0
        
        query = """
            INSERT INTO raw.prices (
                symbol, timeframe, timestamp, open, high, low, close, volume
            ) VALUES (
                %(symbol)s, %(timeframe)s, %(timestamp)s, 
                %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s
            )
            ON CONFLICT (symbol, timeframe, timestamp) 
            DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
        """
        
        with self.asset_conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query, prices)
        
        return len(prices)
    
    def sync_once(self) -> int:
        """Perform one sync cycle"""
        try:
            # Get last sync timestamp
            last_ts = self.get_last_sync_timestamp()
            logger.info(f"Ì¥Ñ Syncing prices since: {last_ts}")
            
            # Fetch new prices
            prices = self.fetch_new_prices(last_ts)
            
            if not prices:
                logger.info("‚ÑπÔ∏è No new prices to sync")
                return 0
            
            # Upsert to asset warehouse
            count = self.upsert_prices(prices)
            
            # Update sync state with latest timestamp
            latest_ts = prices[-1]['timestamp']
            self.update_sync_state(latest_ts)
            
            logger.info(f"‚úÖ Synced {count} price records (up to {latest_ts})")
            return count
            
        except Exception as e:
            logger.error(f"‚ùå Sync error: {e}")
            return 0
    
    def run_continuous(self):
        """Run the synchronizer continuously"""
        logger.info("Ì∫Ä Starting Price Synchronizer Service")
        logger.info(f"Ì≥ä Batch size: {self.batch_size}")
        logger.info(f"‚è±Ô∏è  Sync interval: {config.sync_interval_seconds}s")
        
        try:
            self.connect()
            
            while True:
                try:
                    self.sync_once()
                    time.sleep(config.sync_interval_seconds)
                except KeyboardInterrupt:
                    logger.info("Ìªë Service stopped by user")
                    break
                except Exception as e:
                    logger.error(f"‚ùå Error in sync loop: {e}")
                    time.sleep(10)
                    
        except Exception as e:
            logger.error(f"‚ùå Fatal error: {e}")
        finally:
            if self.core_conn:
                self.core_conn.close()
            if self.asset_conn:
                self.asset_conn.close()
            logger.info("Ì±ã Service shutdown complete")

if __name__ == "__main__":
    synchronizer = PriceSynchronizer()
    synchronizer.run_continuous()
