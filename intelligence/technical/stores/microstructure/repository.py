import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from intelligence.technical.contracts import TickRequest, VolumeRequest
from intelligence.technical.data_access import MicrostructureDataProvider


class PostgresMicrostructureRepository(MicrostructureDataProvider):
    def __init__(self, connection_string: str):
        self.conn_string = connection_string
        self._engine: Engine = None

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(self.conn_string, pool_size=5, max_overflow=10)
        return self._engine

    def get_ticks(self, request: TickRequest) -> pd.DataFrame:
        query = text("""
        SELECT time, symbol, price, volume, bid, ask
        FROM technical_microstructure.ticks
        WHERE symbol = :symbol AND time >= :start AND time <= :end
        ORDER BY time ASC
        LIMIT :limit
        """)
        with self.engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn,
                params={
                    "symbol": request.symbol,
                    "start": request.start,
                    "end": request.end,
                    "limit": request.max_ticks,
                },
                parse_dates=["time"],
            )
        return df

    def get_volume_bars(self, request: VolumeRequest) -> pd.DataFrame:
        query = text("""
        SELECT time_bucket(:aggregate, time) as bucket,
               symbol,
               SUM(volume) as volume,
               AVG(price) as avg_price,
               MIN(price) as low,
               MAX(price) as high
        FROM technical_microstructure.ticks
        WHERE symbol = :symbol AND time >= :start AND time <= :end
        GROUP BY bucket, symbol
        ORDER BY bucket ASC
        """)
        with self.engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn,
                params={
                    "aggregate": request.aggregate,
                    "symbol": request.symbol,
                    "start": request.start,
                    "end": request.end,
                },
                parse_dates=["bucket"],
            )
        return df

    def get_latest_tick(self, symbol: str) -> dict:
        query = text("""
        SELECT time, price, volume, bid, ask
        FROM technical_microstructure.ticks
        WHERE symbol = :symbol
        ORDER BY time DESC LIMIT 1
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"symbol": symbol}).first()
        return dict(result._mapping) if result else None
