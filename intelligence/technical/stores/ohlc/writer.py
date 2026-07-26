import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


class OHLCWriter:
    def __init__(self, connection_string: str):
        self.conn_string = connection_string

    def write_bars(self, df: pd.DataFrame, timeframe: str):
        required = ["symbol", "time", "open", "high", "low", "close", "volume"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        records = [
            (
                row["symbol"],
                row["time"],
                timeframe,
                row["open"],
                row["high"],
                row["low"],
                row["close"],
                row["volume"],
            )
            for _, row in df.iterrows()
        ]

        query = """
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
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                execute_values(cur, query, records)
            conn.commit()
