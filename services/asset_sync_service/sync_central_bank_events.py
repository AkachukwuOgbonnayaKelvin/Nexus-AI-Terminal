"""
Central Bank Events Synchronizer - Copies from nexus_ai_terminal.central_bank_events to raw.central_bank_events
"""
import json
import logging
from datetime import datetime

import psycopg2
import psycopg2.extras

from services.asset_sync_service.config import config

logger = logging.getLogger(__name__)

class CentralBankEventsSynchronizer:
    def __init__(self):
        self.core_conn = None
        self.asset_conn = None
        self.batch_size = config.batch_size

    def connect(self):
        self.core_conn = psycopg2.connect(
            host=config.core_host,
            port=config.core_port,
            dbname='nexus_ai_terminal',
            user=config.core_user,
            password=config.core_password
        )
        self.core_conn.autocommit = True
        logger.info("Connected to core database: nexus_ai_terminal")

        self.asset_conn = psycopg2.connect(
            host=config.asset_host,
            port=config.asset_port,
            dbname=config.asset_dbname,
            user=config.asset_user,
            password=config.asset_password
        )
        self.asset_conn.autocommit = True
        logger.info("Connected to asset database: %s", config.asset_dbname)

    def get_last_sync_timestamp(self):
        with self.asset_conn.cursor() as cur:
            cur.execute("""
                SELECT last_timestamp FROM raw.sync_state WHERE stream_name = 'central_bank_events'
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
                WHERE stream_name = 'central_bank_events'
            """, (last_timestamp,))

    def fetch_new_events(self, since):
        query = """
            SELECT *
            FROM central_bank_events
            WHERE created_at > %s
            ORDER BY created_at ASC
            LIMIT %s
        """
        with self.core_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (since, self.batch_size))
            return cur.fetchall()

    def upsert_events(self, events):
        if not events:
            return 0

        # Convert dict fields to JSON strings
        for event in events:
            if 'metadata' in event and event['metadata'] is not None:
                event['metadata'] = json.dumps(event['metadata'])

        # Use event_id as conflict key
        columns = list(events[0].keys())
        placeholders = ', '.join([f'%({col})s' for col in columns])
        update_cols = [col for col in columns if col not in ['event_id', 'created_at']]
        update_set = ', '.join([f'{col} = EXCLUDED.{col}' for col in update_cols])

        query = f"""
            INSERT INTO raw.central_bank_events ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT (event_id) DO UPDATE SET
                {update_set}
        """
        with self.asset_conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query, events)
        return len(events)

    def sync_once(self):
        try:
            last_ts = self.get_last_sync_timestamp()
            logger.info("Syncing central bank events since: %s", last_ts)

            events = self.fetch_new_events(last_ts)
            if not events:
                logger.info("No new central bank events to sync")
                return 0

            count = self.upsert_events(events)
            latest_ts = events[-1]['created_at']
            self.update_sync_state(latest_ts)

            logger.info("Synced %d central bank events (up to %s)", count, latest_ts)
            return count

        except Exception as e:
            logger.error("Sync error: %s", e)
            return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sync = CentralBankEventsSynchronizer()
    sync.connect()
    count = sync.sync_once()
    print(f"Synced {count} central bank events.")
    sync.core_conn.close()
    sync.asset_conn.close()
