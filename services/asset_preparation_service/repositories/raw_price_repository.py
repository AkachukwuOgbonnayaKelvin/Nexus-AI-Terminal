import psycopg2
import psycopg2.extras
from datetime import datetime
from typing import List, Dict, Any

class RawPriceRepository:
    def __init__(self, conn):
        self.conn = conn

    def fetch_new_bars(self, timeframe: str, since: datetime, limit: int) -> List[Dict[str, Any]]:
        """
        Fetch bars from raw.prices for a given timeframe that are newer than `since`.
        """
        query = """
            SELECT symbol, timestamp, open, high, low, close, volume
            FROM raw.prices
            WHERE UPPER(timeframe) = UPPER(%s)
              AND timestamp > %s
            ORDER BY timestamp ASC
            LIMIT %s
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (timeframe, since, limit))
            return cur.fetchall()

    def get_timeframe_coverage(self, timeframe: str) -> Dict[str, Any]:
        """
        Get summary stats for a given timeframe from raw.prices.
        """
        query = """
            SELECT
                COUNT(*) AS records,
                COUNT(DISTINCT symbol) AS symbols,
                MIN(timestamp) AS first_time,
                MAX(timestamp) AS last_time
            FROM raw.prices
            WHERE UPPER(timeframe) = UPPER(%s)
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (timeframe,))
            return cur.fetchone()
