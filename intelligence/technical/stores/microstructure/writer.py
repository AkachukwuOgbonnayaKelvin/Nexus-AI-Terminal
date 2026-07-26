import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


class MicrostructureWriter:
    def __init__(self, connection_string: str):
        self.conn_string = connection_string

    def write_ticks(self, df: pd.DataFrame):
        required = ["symbol", "time", "price"]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        if "volume" not in df.columns:
            df["volume"] = 0
        if "bid" not in df.columns:
            df["bid"] = None
        if "ask" not in df.columns:
            df["ask"] = None

        records = [
            (
                row["symbol"],
                row["time"],
                row["price"],
                row["volume"],
                row["bid"],
                row["ask"],
            )
            for _, row in df.iterrows()
        ]

        query = """
        INSERT INTO technical_microstructure.ticks
            (symbol, time, price, volume, bid, ask)
        VALUES %s
        ON CONFLICT (symbol, time) DO UPDATE SET
            price = EXCLUDED.price,
            volume = EXCLUDED.volume,
            bid = EXCLUDED.bid,
            ask = EXCLUDED.ask
        """
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                execute_values(cur, query, records)
            conn.commit()
