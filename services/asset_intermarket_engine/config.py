import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class IntermarketConfig:
    asset_host: str = os.getenv('ASSET_DB_HOST', 'localhost')
    asset_port: int = int(os.getenv('ASSET_DB_PORT', 5432))
    asset_dbname: str = os.getenv('ASSET_DB_NAME', 'nexus_asset')
    asset_user: str = os.getenv('ASSET_DB_USER', 'postgres')
    asset_password: str = os.getenv('ASSET_DB_PASSWORD', '6468')

    # Lookback for correlations (in days)
    correlation_window: int = 30

config = IntermarketConfig()
