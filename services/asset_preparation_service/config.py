import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class PrepConfig:
    # Asset database connection
    asset_host: str = os.getenv('ASSET_DB_HOST', 'localhost')
    asset_port: int = int(os.getenv('ASSET_DB_PORT', 5432))
    asset_dbname: str = os.getenv('ASSET_DB_NAME', 'nexus_asset')
    asset_user: str = os.getenv('ASSET_DB_USER', 'postgres')
    asset_password: str = os.getenv('ASSET_DB_PASSWORD', '6468')

    # Timeframes to process (list of strings, all lowercase)
    timeframes: list = None

    # Batch size for fetching from raw and inserting into prepared
    batch_size: int = 10000

    def __post_init__(self):
        if self.timeframes is None:
            self.timeframes = ['m5', 'm15', 'h1', 'h4', 'd1', 'w1', 'mn1']

config = PrepConfig()
