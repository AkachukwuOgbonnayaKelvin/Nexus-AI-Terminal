import logging
from datetime import datetime
from services.asset_preparation_service.repositories.raw_price_repository import RawPriceRepository
from services.asset_preparation_service.repositories.prepared_candle_repository import PreparedCandleRepository
from services.asset_preparation_service.config import config

logger = logging.getLogger(__name__)

class CandleBuilder:
    """
    Generic builder for a single timeframe.
    It reads from raw.prices and writes to prepared.candles_{timeframe}.
    It uses raw.sync_state to track the last processed timestamp for that timeframe.
    """
    def __init__(self, conn):
        self.conn = conn
        self.raw_repo = RawPriceRepository(conn)
        self.prep_repo = PreparedCandleRepository(conn)

    def get_last_processed_timestamp(self, timeframe: str) -> datetime:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT last_timestamp FROM raw.sync_state
                WHERE stream_name = %s
            """, (f"prepared_{timeframe}",))
            row = cur.fetchone()
            if row and row[0]:
                return row[0]
            return datetime(2000, 1, 1)

    def update_processed_timestamp(self, timeframe: str, last_timestamp: datetime):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO raw.sync_state (stream_name, last_timestamp, updated_at)
                VALUES (%s, %s, NOW())
                ON CONFLICT (stream_name) DO UPDATE SET
                    last_timestamp = EXCLUDED.last_timestamp,
                    updated_at = NOW()
            """, (f"prepared_{timeframe}", last_timestamp))

    def build(self, timeframe: str) -> int:
        """
        Build prepared candles for one timeframe incrementally.
        Processes all available rows in batches (as defined by config.batch_size).
        Returns the total number of candles upserted in this run.
        """
        logger.info("Building prepared candles for %s", timeframe)

        since = self.get_last_processed_timestamp(timeframe)
        logger.info("Processing %s since %s", timeframe, since)

        total_upserted = 0
        while True:
            # Fetch a batch
            bars = self.raw_repo.fetch_new_bars(timeframe, since, config.batch_size)
            if not bars:
                break

            # Upsert
            count = self.prep_repo.upsert_candles(timeframe, bars)
            total_upserted += count

            # Update the processed timestamp to the latest bar in this batch
            latest_ts = bars[-1]['timestamp']
            self.update_processed_timestamp(timeframe, latest_ts)

            # Set since to the last timestamp for the next iteration
            since = latest_ts
            logger.info("Upserted %d candles for %s (up to %s), total %d", count, timeframe, latest_ts, total_upserted)

            # If we got fewer than batch_size, we've reached the end
            if len(bars) < config.batch_size:
                break

        logger.info("Completed %s: total upserted %d", timeframe, total_upserted)
        return total_upserted
