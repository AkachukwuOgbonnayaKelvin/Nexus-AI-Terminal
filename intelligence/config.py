import os

DATABASE_TYPE = os.getenv("NEXUS_DB_TYPE", "sqlite")  # 'sqlite' or 'postgresql'

if DATABASE_TYPE == "postgresql":
    DATABASE_URL = f"postgresql://postgres:{os.getenv('PGPASSWORD', '6468')}@localhost/nexus_ai_terminal"
    ENGINE_TYPE = "postgresql"
    SCHEMA = "raw"
    # Table names in PostgreSQL
    TICK_TABLE = "raw.market_ticks"
    OHLCV_TABLE = "raw.market_ohlcv"
    VOLUME_TABLE = "raw.market_volume"
    AGGREGATED_TABLE = "raw.tick_aggregates"
else:
    DATABASE_URL = "sqlite:///nexus_data.db"
    ENGINE_TYPE = "sqlite"
    SCHEMA = None
    TICK_TABLE = "fact_tick"
    OHLCV_TABLE = "fact_ohlcv"
    VOLUME_TABLE = "fact_volume"
    AGGREGATED_TABLE = "fact_tick_aggregated"
