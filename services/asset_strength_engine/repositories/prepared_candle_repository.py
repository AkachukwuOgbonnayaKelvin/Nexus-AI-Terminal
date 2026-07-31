import psycopg2
import psycopg2.extras
from typing import List, Dict, Any

class PreparedCandleRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_closing_prices(self, symbol: str, timeframe: str, limit: int) -> List[float]:
        """
        Fetch the last `limit` closing prices for a given symbol and timeframe.
        """
        table_name = f"prepared.candles_{timeframe.lower()}"
        query = f"""
            SELECT close
            FROM {table_name}
            WHERE symbol = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (symbol, limit))
            rows = cur.fetchall()
            return [float(row[0]) for row in rows if row[0] is not None]

    def get_symbols(self, timeframe: str) -> List[str]:
        """
        Get all symbols available in a given timeframe's prepared table.
        """
        table_name = f"prepared.candles_{timeframe.lower()}"
        query = f"SELECT DISTINCT symbol FROM {table_name} ORDER BY symbol;"
        with self.conn.cursor() as cur:
            cur.execute(query)
            return [row[0] for row in cur.fetchall()]
