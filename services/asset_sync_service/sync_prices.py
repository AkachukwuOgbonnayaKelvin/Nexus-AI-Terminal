"""
Price Synchronizer - Copies data from core.prices to raw.prices
"""
import time
import logging
from datetime import datetime
from typing import List, Dict, Any

import psycopg2
import psycopg2.extras

from services.asset_sync_service.config import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PriceSynchronizer:
    """Synchronizes price data from core to asset warehouse."""

    def __init__(self):
        self.core_conn = None
        self.asset_conn = None
        self.batch_size = config.batch_size

    def connect(self):
        try:
            self.core_conn = psycopg2.connect(
                host=config.core_host,
                port=config.core_port,
                dbname=config.core_dbname,
                user=config.core_user,
                password=config.core_password
            )
            self.core_conn.autocommit = True
            logger.info("Connected to core database: %s", config.core_dbname)

            self.asset_conn = psycopg2.connect(
                host=config.asset_host,
                port=config.asset_port,
                dbname=config.asset_dbname,
                user=config.asset_user,
                password=config.asset_password
            )
            self.asset_conn.autocommit = True
            logger.info("Connected to asset database: %s", config.asset_dbname)

        except Exception as e:
            logger.error("Connection error: %s", e)
            raise

    def get_last_sync_timestamp(self):
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

    def update_sync_state(self, last_timestamp):
        with self.asset_conn.cursor() as cur:
            cur.execute("""
                UPDATE raw.sync_state
                SET last_timestamp = %s, updated_at = NOW()
                WHERE stream_name = 'prices'
            """, (last_timestamp,))

    def fetch_new_prices(self, since):
        query = """
            SELECT symbol, timeframe, timestamp, open, high, low, close, volume
            FROM prices
            WHERE timestamp > %s
            ORDER BY timestamp ASC
            LIMIT %s
        """
        with self.core_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (since, self.batch_size))
            return cur.fetchall()

    def upsert_prices(self, prices):
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

    def sync_once(self):
        try:
            last_ts = self.get_last_sync_timestamp()
            logger.info("Syncing prices since: %s", last_ts)

            prices = self.fetch_new_prices(last_ts)
            if not prices:
                logger.info("No new prices to sync")
                return 0

            count = self.upsert_prices(prices)
            latest_ts = prices[-1]['timestamp']
            self.update_sync_state(latest_ts)

            logger.info("Synced %d price records (up to %s)", count, latest_ts)
            return count

        except Exception as e:
            logger.error("Sync error: %s", e)
            return 0

    def run_continuous(self):
        logger.info("Starting Price Synchronizer Service")
        logger.info("Batch size: %d", self.batch_size)
        logger.info("Sync interval: %d s", config.sync_interval_seconds)

        try:
            self.connect()
            while True:
                try:
                    self.sync_once()
                    time.sleep(config.sync_interval_seconds)
                except KeyboardInterrupt:
                    logger.info("Service stopped by user")
                    break
                except Exception as e:
                    logger.error("Error in sync loop: %s", e)
                    time.sleep(10)

        except Exception as e:
            logger.error("Fatal error: %s", e)
        finally:
            if self.core_conn:
                self.core_conn.close()
            if self.asset_conn:
                self.asset_conn.close()
            logger.info("Service shutdown complete")


if __name__ == "__main__":
    synchronizer = PriceSynchronizer()
    synchronizer.run_continuous()
