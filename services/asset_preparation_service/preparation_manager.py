import logging
from datetime import datetime
import psycopg2

from services.asset_preparation_service.config import config
from services.asset_preparation_service.builders.candle_builder import CandleBuilder
from services.asset_preparation_service.repositories.raw_price_repository import RawPriceRepository
from services.asset_preparation_service.repositories.prepared_candle_repository import PreparedCandleRepository

logger = logging.getLogger(__name__)

class PreparationManager:
    def __init__(self):
        self.conn = None
        self.builder = None
        self.raw_repo = None
        self.prep_repo = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=config.asset_host,
            port=config.asset_port,
            dbname=config.asset_dbname,
            user=config.asset_user,
            password=config.asset_password
        )
        self.conn.autocommit = True
        logger.info("Connected to asset database: %s", config.asset_dbname)
        self.builder = CandleBuilder(self.conn)
        self.raw_repo = RawPriceRepository(self.conn)
        self.prep_repo = PreparedCandleRepository(self.conn)

    def update_status(self, timeframe: str):
        """
        Update the timeframe_status table with current coverage stats.
        """
        raw_stats = self.raw_repo.get_timeframe_coverage(timeframe)
        prep_stats = self.prep_repo.get_coverage(timeframe)

        status = "READY"
        if raw_stats['records'] is None or raw_stats['records'] == 0:
            status = "NO_SOURCE_DATA"
        elif prep_stats['records'] is None or prep_stats['records'] == 0:
            status = "NOT_PREPARED"
        elif prep_stats['records'] < raw_stats['records']:
            status = "PARTIAL"
        # else "READY"

        query = """
            INSERT INTO prepared.timeframe_status (
                timeframe, source_records, prepared_records, symbols,
                first_time, last_time, status, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, NOW()
            ) ON CONFLICT (timeframe) DO UPDATE SET
                source_records = EXCLUDED.source_records,
                prepared_records = EXCLUDED.prepared_records,
                symbols = EXCLUDED.symbols,
                first_time = EXCLUDED.first_time,
                last_time = EXCLUDED.last_time,
                status = EXCLUDED.status,
                updated_at = NOW()
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (
                timeframe,
                raw_stats['records'],
                prep_stats['records'],
                raw_stats['symbols'],  # we use raw symbols as the definitive list
                raw_stats['first_time'],
                raw_stats['last_time'],
                status
            ))

    def run(self):
        self.connect()
        logger.info("Starting Preparation Manager")
        for tf in config.timeframes:
            # Build candles for this timeframe
            try:
                count = self.builder.build(tf)
                logger.info("Built %d candles for %s", count, tf)
            except Exception as e:
                logger.error("Failed to build %s: %s", tf, e)
                # Update status to ERROR if needed, but we'll just log for now

            # Update status
            self.update_status(tf)

        self.conn.close()
        logger.info("Preparation Manager finished")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = PreparationManager()
    manager.run()
