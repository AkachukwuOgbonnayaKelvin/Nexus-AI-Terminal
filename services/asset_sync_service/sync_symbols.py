"""
Symbols Synchronizer - Copies from nexus_data.symbols to raw.symbols
"""
import time
import logging
from datetime import datetime

import psycopg2
import psycopg2.extras

from services.asset_sync_service.config import config

logger = logging.getLogger(__name__)

class SymbolsSynchronizer:
    def __init__(self):
        self.core_conn = None
        self.asset_conn = None
        self.batch_size = config.batch_size

    def connect(self):
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

    def get_last_sync_id(self):
        with self.asset_conn.cursor() as cur:
            cur.execute("""
                SELECT last_id FROM raw.sync_state WHERE stream_name = 'symbols'
            """)
            result = cur.fetchone()
            if result and result[0]:
                return result[0]
            return 0

    def update_sync_state(self, last_id):
        with self.asset_conn.cursor() as cur:
            cur.execute("""
                UPDATE raw.sync_state
                SET last_id = %s, last_timestamp = NOW(), updated_at = NOW()
                WHERE stream_name = 'symbols'
            """, (last_id,))

    def fetch_new_symbols(self, since_id):
        query = """
            SELECT id, symbol, asset_type, description, currency, exchange, active, created_at
            FROM symbols
            WHERE id > %s
            ORDER BY id ASC
            LIMIT %s
        """
        with self.core_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (since_id, self.batch_size))
            return cur.fetchall()

    def upsert_symbols(self, symbols):
        if not symbols:
            return 0

        query = """
            INSERT INTO raw.symbols (
                id, symbol, asset_type, description, currency, exchange, active, created_at
            ) VALUES (
                %(id)s, %(symbol)s, %(asset_type)s, %(description)s,
                %(currency)s, %(exchange)s, %(active)s, %(created_at)s
            )
            ON CONFLICT (symbol) DO UPDATE SET
                asset_type = EXCLUDED.asset_type,
                description = EXCLUDED.description,
                currency = EXCLUDED.currency,
                exchange = EXCLUDED.exchange,
                active = EXCLUDED.active,
                created_at = EXCLUDED.created_at
        """
        with self.asset_conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query, symbols)
        return len(symbols)

    def sync_once(self):
        try:
            last_id = self.get_last_sync_id()
            logger.info("Syncing symbols since id: %s", last_id)

            symbols = self.fetch_new_symbols(last_id)
            if not symbols:
                logger.info("No new symbols to sync")
                return 0

            count = self.upsert_symbols(symbols)
            latest_id = symbols[-1]['id']
            self.update_sync_state(latest_id)

            logger.info("Synced %d symbols (up to id %s)", count, latest_id)
            return count

        except Exception as e:
            logger.error("Sync error: %s", e)
            return 0

    def run_continuous(self):
        # same as PriceSynchronizer
        pass

if __name__ == "__main__":
    sync = SymbolsSynchronizer()
    sync.connect()
    count = sync.sync_once()
    print(f"Synced {count} symbols.")
    sync.core_conn.close()
    sync.asset_conn.close()
