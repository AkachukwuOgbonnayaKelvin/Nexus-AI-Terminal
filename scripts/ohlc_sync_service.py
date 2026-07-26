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
    handlers=[logging.FileHandler("logs/ohlc_sync.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

DB_CONN = "postgresql://postgres:6468@localhost:5432/nexus_ai_terminal"

# Configuration
SYNC_INTERVAL_SECONDS = 300  # 5 minutes
MAX_RETRIES = 3
BATCH_SIZE = 1000

# Flag to stop gracefully
shutdown_flag = False


def signal_handler(sig, frame):
    global shutdown_flag
    logger.info("Received shutdown signal. Stopping gracefully...")
    shutdown_flag = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class OHLCDataSyncError(Exception):
    pass


class OHLCDataSyncService:
    def __init__(self, conn_string: str):
        self.conn_string = conn_string
        self.running = False

    def get_connection(self):
        return psycopg2.connect(self.conn_string)

    def get_available_timeframes(self, conn) -> list[tuple[str, str]]:
        """Get all symbol/timeframe pairs from raw"""
        query = """
        SELECT DISTINCT symbol, timeframe
        FROM raw.market_ohlcv
        ORDER BY symbol, timeframe
        """
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_sync_state(self, conn, symbol: str, timeframe: str):
        """Get the last synced time for a symbol/timeframe"""
        query = """
        SELECT last_raw_time, last_synced_at
        FROM technical_ohlc.sync_state
        WHERE symbol = %s AND timeframe = %s
        """
        with conn.cursor() as cur:
            cur.execute(query, (symbol, timeframe))
            result = cur.fetchone()
        return result

    def update_sync_state(
        self,
        conn,
        symbol: str,
        timeframe: str,
        last_raw_time,
        raw_count: int,
        tech_count: int,
        status: str = "HEALTHY",
        error: str = None,
    ):
        """Update sync state for a symbol/timeframe"""
        query = """
        INSERT INTO technical_ohlc.sync_state
            (symbol, timeframe, last_raw_time, last_synced_at, raw_count, technical_count, status, error_message, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, timeframe) DO UPDATE SET
            last_raw_time = EXCLUDED.last_raw_time,
            last_synced_at = EXCLUDED.last_synced_at,
            raw_count = EXCLUDED.raw_count,
            technical_count = EXCLUDED.technical_count,
            status = EXCLUDED.status,
            error_message = EXCLUDED.error_message,
            updated_at = EXCLUDED.updated_at
        """
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    symbol,
                    timeframe,
                    last_raw_time,
                    datetime.now(),
                    raw_count,
                    tech_count,
                    status,
                    error,
                    datetime.now(),
                ),
            )
        conn.commit()

    def sync_symbol_timeframe(self, conn, symbol: str, timeframe: str) -> bool:
        """
        Synchronize one symbol/timeframe pair.
        Returns True if successful, False otherwise.
        """
        try:
            # Get current raw data
            raw_count_query = """
            SELECT COUNT(*), MAX(time)
            FROM raw.market_ohlcv
            WHERE symbol = %s AND timeframe = %s
            """
            with conn.cursor() as cur:
                cur.execute(raw_count_query, (symbol, timeframe))
                raw_count, raw_max_time = cur.fetchone()

            if raw_count == 0:
                logger.warning(f"No raw data for {symbol} {timeframe}")
                return False

            # Get last sync state
            state = self.get_sync_state(conn, symbol, timeframe)
            if state:
                last_raw_time = state[0]
            else:
                last_raw_time = None

            # Determine if we need to sync
            if last_raw_time and raw_max_time <= last_raw_time:
                logger.debug(f"No new data for {symbol} {timeframe}")
                # Still update counts
                tech_count = self.get_technical_count(conn, symbol, timeframe)
                self.update_sync_state(
                    conn, symbol, timeframe, raw_max_time, raw_count, tech_count
                )
                return True

            # Fetch new data
            if last_raw_time:
                query = """
                SELECT symbol, time, open, high, low, close, volume
                FROM raw.market_ohlcv
                WHERE symbol = %s AND timeframe = %s AND time > %s
                ORDER BY time
                """
                with conn.cursor() as cur:
                    cur.execute(query, (symbol, timeframe, last_raw_time))
                    rows = cur.fetchall()
            else:
                query = """
                SELECT symbol, time, open, high, low, close, volume
                FROM raw.market_ohlcv
                WHERE symbol = %s AND timeframe = %s
                ORDER BY time
                """
                with conn.cursor() as cur:
                    cur.execute(query, (symbol, timeframe))
                    rows = cur.fetchall()

            if not rows:
                logger.debug(f"No new rows for {symbol} {timeframe}")
                return True

            # Upsert in batches
            total_inserted = 0
            for i in range(0, len(rows), BATCH_SIZE):
                batch = rows[i : i + BATCH_SIZE]
                records = [
                    (
                        row[0],
                        row[1],
                        timeframe,
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6] if row[6] is not None else 0,
                    )
                    for row in batch
                ]
                insert_sql = """
                INSERT INTO technical_ohlc.bars
                    (symbol, time, timeframe, open, high, low, close, volume)
                VALUES %s
                ON CONFLICT (symbol, time, timeframe) DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    volume = EXCLUDED.volume,
                    updated_at = CURRENT_TIMESTAMP
                """
                with conn.cursor() as cur:
                    execute_values(cur, insert_sql, records)
                conn.commit()
                total_inserted += len(records)

            # Verify counts
            tech_count = self.get_technical_count(conn, symbol, timeframe)
            if tech_count != raw_count:
                logger.warning(
                    f"Count mismatch for {symbol} {timeframe}: raw={raw_count}, tech={tech_count}"
                )
                self.update_sync_state(
                    conn,
                    symbol,
                    timeframe,
                    raw_max_time,
                    raw_count,
                    tech_count,
                    "COUNT_MISMATCH",
                )
                return True

            # Update sync state
            self.update_sync_state(
                conn, symbol, timeframe, raw_max_time, raw_count, tech_count
            )
            logger.info(
                f"Synced {symbol} {timeframe}: {total_inserted} new rows inserted, total={tech_count}"
            )
            return True

        except Exception as e:
            logger.error(f"Error syncing {symbol} {timeframe}: {e}")
            # Try to update state with error
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE technical_ohlc.sync_state
                        SET status = 'ERROR', error_message = %s, updated_at = %s
                        WHERE symbol = %s AND timeframe = %s
                    """,
                        (str(e), datetime.now(), symbol, timeframe),
                    )
                conn.commit()
            except:
                pass
            return False

    def get_technical_count(self, conn, symbol: str, timeframe: str) -> int:
        query = "SELECT COUNT(*) FROM technical_ohlc.bars WHERE symbol = %s AND timeframe = %s"
        with conn.cursor() as cur:
            cur.execute(query, (symbol, timeframe))
            return cur.fetchone()[0]

    def run_sync_cycle(self):
        """Run one full synchronization cycle"""
        logger.info("Starting sync cycle...")
        try:
            with self.get_connection() as conn:
                pairs = self.get_available_timeframes(conn)
                logger.info(f"Found {len(pairs)} symbol/timeframe pairs to sync")

                success_count = 0
                for symbol, timeframe in pairs:
                    if self.sync_symbol_timeframe(conn, symbol, timeframe):
                        success_count += 1

                logger.info(
                    f"Sync cycle completed: {success_count}/{len(pairs)} pairs synced successfully"
                )
                return success_count == len(pairs)

        except Exception as e:
            logger.error(f"Sync cycle failed: {e}")
            return False

    def run_forever(self):
        """Run the sync service continuously"""
        self.running = True
        logger.info(
            f"OHLC Sync Service started. Sync interval: {SYNC_INTERVAL_SECONDS}s"
        )

        while self.running and not shutdown_flag:
            try:
                self.run_sync_cycle()
                # Wait for next cycle
                for _ in range(SYNC_INTERVAL_SECONDS):
                    if shutdown_flag:
                        break
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Unhandled error in sync service: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

        logger.info("OHLC Sync Service stopped.")

    def stop(self):
        self.running = False


def main():
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    service = OHLCDataSyncService(DB_CONN)
    service.run_forever()


if __name__ == "__main__":
    main()
