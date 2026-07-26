import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import signal
import time
from datetime import datetime

import psycopg2
from psycopg2.extras import execute_values

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/tick_sync.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

SYNC_INTERVAL_SECONDS = 300
BATCH_SIZE = 10000
shutdown_flag = False


def signal_handler(sig, frame):
    global shutdown_flag
    logger.info("Shutting down tick sync service...")
    shutdown_flag = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class TickSyncService:
    def __init__(self, conn_string):
        self.conn_string = conn_string

    def get_connection(self):
        return psycopg2.connect(self.conn_string)

    def get_tick_symbols(self, conn):
        try:
            query = "SELECT DISTINCT symbol FROM raw.market_ticks ORDER BY symbol"
            with conn.cursor() as cur:
                cur.execute(query)
                return [row[0] for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching tick symbols: {e}")
            return []

    def get_sync_state(self, conn, symbol):
        try:
            query = "SELECT last_raw_time FROM technical_microstructure.sync_state WHERE symbol = %s"
            with conn.cursor() as cur:
                cur.execute(query, (symbol,))
                result = cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Error getting sync state for {symbol}: {e}")
            return None

    def update_sync_state(
        self, conn, symbol, last_raw_time, raw_count, tech_count, status="HEALTHY"
    ):
        try:
            query = """
            INSERT INTO technical_microstructure.sync_state
                (symbol, last_raw_time, last_synced_at, raw_count, technical_count, status, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE SET
                last_raw_time = EXCLUDED.last_raw_time,
                last_synced_at = EXCLUDED.last_synced_at,
                raw_count = EXCLUDED.raw_count,
                technical_count = EXCLUDED.technical_count,
                status = EXCLUDED.status,
                updated_at = EXCLUDED.updated_at
            """
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        symbol,
                        last_raw_time,
                        datetime.now(),
                        raw_count,
                        tech_count,
                        status,
                        datetime.now(),
                    ),
                )
            conn.commit()
        except Exception as e:
            logger.error(f"Error updating sync state for {symbol}: {e}")

    def sync_symbol(self, conn, symbol):
        try:
            # Get raw count and max time
            raw_query = """
            SELECT COUNT(*), MAX(time)
            FROM raw.market_ticks
            WHERE symbol = %s
            """
            with conn.cursor() as cur:
                cur.execute(raw_query, (symbol,))
                raw_count, raw_max_time = cur.fetchone()

            if raw_count == 0:
                logger.warning(f"No ticks for {symbol}")
                return

            last_time = self.get_sync_state(conn, symbol)

            if last_time and raw_max_time <= last_time:
                logger.debug(f"No new ticks for {symbol}")
                tech_count = self.get_technical_count(conn, symbol)
                self.update_sync_state(
                    conn, symbol, raw_max_time, raw_count, tech_count
                )
                return

            # Fetch new ticks from raw, using COALESCE to handle nulls
            # Price = COALESCE(last, (bid + ask)/2) but ensure price > 0
            if last_time:
                query = """
                SELECT time, symbol,
                       COALESCE(last, (bid + ask) / 2) as price,
                       volume, bid, ask
                FROM raw.market_ticks
                WHERE symbol = %s AND time > %s
                  AND (last IS NOT NULL OR (bid IS NOT NULL AND ask IS NOT NULL))
                ORDER BY time
                """
                with conn.cursor() as cur:
                    cur.execute(query, (symbol, last_time))
                    rows = cur.fetchall()
            else:
                query = """
                SELECT time, symbol,
                       COALESCE(last, (bid + ask) / 2) as price,
                       volume, bid, ask
                FROM raw.market_ticks
                WHERE symbol = %s
                  AND (last IS NOT NULL OR (bid IS NOT NULL AND ask IS NOT NULL))
                ORDER BY time
                """
                with conn.cursor() as cur:
                    cur.execute(query, (symbol,))
                    rows = cur.fetchall()

            if not rows:
                logger.info(f"No valid price rows for {symbol}")
                return

            total = 0
            for i in range(0, len(rows), BATCH_SIZE):
                batch = rows[i : i + BATCH_SIZE]
                records = [
                    (
                        row[0],
                        row[1],
                        row[2],
                        row[3] if row[3] is not None else 0,
                        row[4] if row[4] is not None else None,
                        row[5] if row[5] is not None else None,
                    )
                    for row in batch
                    if row[2] is not None and row[2] > 0
                ]
                if not records:
                    continue
                insert_sql = """
                INSERT INTO technical_microstructure.ticks
                    (time, symbol, price, volume, bid, ask)
                VALUES %s
                ON CONFLICT (symbol, time) DO UPDATE SET
                    price = EXCLUDED.price,
                    volume = EXCLUDED.volume,
                    bid = EXCLUDED.bid,
                    ask = EXCLUDED.ask
                """
                with conn.cursor() as cur:
                    execute_values(cur, insert_sql, records)
                conn.commit()
                total += len(records)

            tech_count = self.get_technical_count(conn, symbol)
            self.update_sync_state(conn, symbol, raw_max_time, raw_count, tech_count)
            logger.info(
                f"Synced {symbol}: inserted {total} valid ticks, total={tech_count}"
            )

        except Exception as e:
            logger.error(f"Error syncing ticks for {symbol}: {e}")
            conn.rollback()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO technical_microstructure.sync_state
                            (symbol, status, error_message, updated_at)
                        VALUES (%s, 'ERROR', %s, %s)
                        ON CONFLICT (symbol) DO UPDATE SET
                            status = 'ERROR',
                            error_message = EXCLUDED.error_message,
                            updated_at = EXCLUDED.updated_at
                    """,
                        (symbol, str(e), datetime.now()),
                    )
                conn.commit()
            except:
                pass

    def get_technical_count(self, conn, symbol):
        query = "SELECT COUNT(*) FROM technical_microstructure.ticks WHERE symbol = %s"
        with conn.cursor() as cur:
            cur.execute(query, (symbol,))
            return cur.fetchone()[0]

    def run_cycle(self):
        logger.info("Starting tick sync cycle...")
        try:
            with self.get_connection() as conn:
                symbols = self.get_tick_symbols(conn)
                if not symbols:
                    logger.warning("No tick symbols found in raw.market_ticks")
                    return
                logger.info(f"Found {len(symbols)} symbols with ticks")
                for sym in symbols:
                    self.sync_symbol(conn, sym)
            logger.info("Tick sync cycle completed.")
        except Exception as e:
            logger.error(f"Tick sync cycle failed: {e}")

    def run_forever(self):
        logger.info(f"Tick sync service started, interval={SYNC_INTERVAL_SECONDS}s")
        while not shutdown_flag:
            try:
                self.run_cycle()
                for _ in range(SYNC_INTERVAL_SECONDS):
                    if shutdown_flag:
                        break
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Unhandled error: {e}")
                time.sleep(60)
        logger.info("Tick sync service stopped.")


def main():
    os.makedirs("logs", exist_ok=True)
    service = TickSyncService(DB_CONN)
    service.run_forever()


if __name__ == "__main__":
    main()
