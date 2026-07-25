"""
Technical Data Access Layer
Provides standardized, query-optimized access to OHLCV data.
"""

import sqlite3
from datetime import datetime

import pandas as pd


class TechnicalDataAccess:
    def __init__(self, db_path: str = "nexus_data.db"):
        self.db_path = db_path

    def _execute_query(self, query: str, params: tuple = ()) -> pd.DataFrame:
        """Execute a query and return a DataFrame."""
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(query, conn, params=params, parse_dates=["time"])

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame:
        """
        Fetch OHLCV candles for a given symbol and timeframe.

        Args:
            symbol: e.g., 'EURUSD'
            timeframe: e.g., 'D1', 'H1', 'M15'
            start: datetime start (inclusive)
            end: datetime end (inclusive)
            limit: max number of rows (if start/end not set, returns latest)

        Returns:
            DataFrame with columns: time, open, high, low, close, volume
        """
        query = """
            SELECT time, open, high, low, close, volume
            FROM fact_ohlcv
            WHERE symbol = ? AND timeframe = ?
        """
        params = [symbol, timeframe]

        if start:
            query += " AND time >= ?"
            params.append(start)
        if end:
            query += " AND time <= ?"
            params.append(end)

        query += " ORDER BY time ASC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        df = self._execute_query(query, tuple(params))
        return df

    def get_latest(self, symbol: str, timeframe: str, n: int = 1) -> pd.DataFrame:
        """Get the latest n candles."""
        return self.get_candles(symbol, timeframe, limit=n)

    def get_multi_timeframe(
        self,
        symbol: str,
        timeframes: list[str],
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 1000,
    ) -> dict[str, pd.DataFrame]:
        """
        Fetch multiple timeframes for the same symbol.
        """
        result = {}
        for tf in timeframes:
            result[tf] = self.get_candles(symbol, tf, start, end, limit)
        return result

    def get_rolling_window(
        self,
        symbol: str,
        timeframe: str,
        window: int = 20,
        start: datetime | None = None,
    ) -> pd.DataFrame:
        """
        Get a rolling window (e.g., for ATR). Returns a DataFrame with additional rolling columns.
        """
        df = self.get_candles(symbol, timeframe, start=start, limit=window + 200)
        if df.empty:
            return df
        # Compute rolling statistics (example: high-low range)
        df["high_low"] = df["high"] - df["low"]
        df["atr"] = df["high_low"].rolling(window).mean()
        return df

    def get_symbols(self) -> list[str]:
        """Return all unique symbols in the warehouse."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT symbol FROM fact_ohlcv ORDER BY symbol")
            return [row[0] for row in cursor.fetchall()]

    def get_timeframes(self, symbol: str | None = None) -> list[str]:
        """
        Return all timeframes available (for a symbol if provided).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if symbol:
                cursor.execute(
                    "SELECT DISTINCT timeframe FROM fact_ohlcv WHERE symbol = ? ORDER BY timeframe",
                    (symbol,),
                )
            else:
                cursor.execute(
                    "SELECT DISTINCT timeframe FROM fact_ohlcv ORDER BY timeframe"
                )
            return [row[0] for row in cursor.fetchall()]

    def get_coverage(self, symbol: str, timeframe: str) -> dict[str, datetime | None]:
        """
        Return earliest and latest timestamps for a symbol/timeframe.
        """
        query = """
            SELECT MIN(time) as earliest, MAX(time) as latest
            FROM fact_ohlcv
            WHERE symbol = ? AND timeframe = ?
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (symbol, timeframe))
            row = cursor.fetchone()
            return {
                "earliest": datetime.fromisoformat(row[0]) if row[0] else None,
                "latest": datetime.fromisoformat(row[1]) if row[1] else None,
            }
