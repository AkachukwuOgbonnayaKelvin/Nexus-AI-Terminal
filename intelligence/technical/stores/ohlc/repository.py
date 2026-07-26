import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from intelligence.technical.contracts import OHLCRequest
from intelligence.technical.data_access import OHLCDataProvider


class PostgresOHLCRepository(OHLCDataProvider):
    def __init__(self, connection_string: str):
        self.conn_string = connection_string
        self._engine: Engine = None

    @property
    def engine(self) -> Engine:
        """Lazy-load SQLAlchemy engine."""
        if self._engine is None:
            self._engine = create_engine(self.conn_string, pool_size=5, max_overflow=10)
        return self._engine

    def get_bars(self, request: OHLCRequest) -> pd.DataFrame:
        query = text("""
        SELECT time, symbol, open, high, low, close, volume
        FROM technical_ohlc.bars
        WHERE symbol = :symbol AND timeframe = :timeframe
          AND time >= :start AND time <= :end
        ORDER BY time ASC
        """)
        with self.engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn,
                params={
                    "symbol": request.symbol,
                    "timeframe": request.timeframe,
                    "start": request.start,
                    "end": request.end,
                },
                parse_dates=["time"],
            )
        return df

    def get_latest_bar(self, symbol: str, timeframe: str) -> dict:
        query = text("""
        SELECT time, open, high, low, close, volume
        FROM technical_ohlc.bars
        WHERE symbol = :symbol AND timeframe = :timeframe
        ORDER BY time DESC LIMIT 1
        """)
        with self.engine.connect() as conn:
            result = conn.execute(
                query, {"symbol": symbol, "timeframe": timeframe}
            ).first()
        return dict(result._mapping) if result else None

    def get_bar_count(self, symbol: str, timeframe: str) -> int:
        query = text("""
        SELECT COUNT(*) FROM technical_ohlc.bars
        WHERE symbol = :symbol AND timeframe = :timeframe
        """)
        with self.engine.connect() as conn:
            return (
                conn.execute(query, {"symbol": symbol, "timeframe": timeframe}).scalar()
                or 0
            )

    def get_time_range(self, symbol: str, timeframe: str) -> tuple:
        """Get min and max time for a symbol/timeframe."""
        query = text("""
        SELECT MIN(time) as min_time, MAX(time) as max_time
        FROM technical_ohlc.bars
        WHERE symbol = :symbol AND timeframe = :timeframe
        """)
        with self.engine.connect() as conn:
            result = conn.execute(
                query, {"symbol": symbol, "timeframe": timeframe}
            ).first()
        return (result.min_time, result.max_time) if result else (None, None)

    def get_last_bars(self, symbol: str, timeframe: str, limit: int) -> pd.DataFrame:
        """Fetch the most recent N bars for a symbol/timeframe."""
        query = text("""
        SELECT time, symbol, open, high, low, close, volume
        FROM technical_ohlc.bars
        WHERE symbol = :symbol AND timeframe = :timeframe
        ORDER BY time DESC
        LIMIT :limit
        """)
        with self.engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn,
                params={"symbol": symbol, "timeframe": timeframe, "limit": limit},
                parse_dates=["time"],
            )
        return df.sort_values("time").reset_index(drop=True)
