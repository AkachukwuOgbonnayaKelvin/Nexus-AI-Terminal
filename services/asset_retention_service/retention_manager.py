"""
Retention Manager - Deletes old data from raw.prices based on timeframe retention policy.
"""
import logging
import psycopg2
from datetime import datetime, timedelta
from services.asset_retention_service.config import config

logger = logging.getLogger(__name__)

class RetentionManager:
    def __init__(self):
        self.conn = None

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

    def get_timeframes(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT DISTINCT timeframe FROM raw.prices;")
            return [row[0] for row in cur.fetchall()]

    def delete_old_bars(self, timeframe: str, retention_days: int):
        cutoff = datetime.utcnow() - timedelta(days=retention_days)
        query = """
            DELETE FROM raw.prices
            WHERE timeframe = %s AND timestamp < %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (timeframe, cutoff))
            deleted = cur.rowcount
            if deleted:
                logger.info("Deleted %d bars for %s (older than %s days)", deleted, timeframe, retention_days)
            return deleted

    def run_retention(self):
        self.connect()
        timeframes = self.get_timeframes()
        logger.info("Applying retention policy to %d timeframes", len(timeframes))
        total_deleted = 0
        for tf in timeframes:
            if tf in config.retention_policy:
                days = config.retention_policy[tf]
                deleted = self.delete_old_bars(tf, days)
                total_deleted += deleted
            else:
                logger.warning("No retention policy defined for timeframe: %s", tf)
        logger.info("Retention complete. Total deleted: %d", total_deleted)
        self.conn.close()
        return total_deleted

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = RetentionManager()
    manager.run_retention()
