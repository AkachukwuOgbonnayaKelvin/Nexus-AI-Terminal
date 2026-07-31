import psycopg2
import psycopg2.extras
from typing import List, Dict, Any

class PreparedCandleRepository:
    def __init__(self, conn):
        self.conn = conn

    def upsert_candles(self, timeframe: str, candles: List[Dict[str, Any]]) -> int:
        if not candles:
            return 0

        table_name = f"prepared.candles_{timeframe}"
        query = f"""
            INSERT INTO {table_name} (symbol, timestamp, open, high, low, close, volume)
            VALUES (%(symbol)s, %(timestamp)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s)
            ON CONFLICT (symbol, timestamp) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
        """
        with self.conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query, candles)
        return len(candles)

    def get_coverage(self, timeframe: str) -> Dict[str, Any]:
        """
        Get summary stats for a given timeframe from prepared candles.
        """
        table_name = f"prepared.candles_{timeframe}"
        query = f"""
            SELECT
                COUNT(*) AS records,
                COUNT(DISTINCT symbol) AS symbols,
                MIN(timestamp) AS first_time,
                MAX(timestamp) AS last_time
            FROM {table_name}
        """
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchone()
