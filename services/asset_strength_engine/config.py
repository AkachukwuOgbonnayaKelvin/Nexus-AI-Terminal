import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class StrengthConfig:
    # Asset database connection
    asset_host: str = os.getenv('ASSET_DB_HOST', 'localhost')
    asset_port: int = int(os.getenv('ASSET_DB_PORT', 5432))
    asset_dbname: str = os.getenv('ASSET_DB_NAME', 'nexus_asset')
    asset_user: str = os.getenv('ASSET_DB_USER', 'postgres')
    asset_password: str = os.getenv('ASSET_DB_PASSWORD', '6468')

    # Timeframes to include in strength calculation
    timeframes: list = None
    # Weights for each timeframe (must sum to 1.0)
    weights: dict = None
    # Lookback periods for Z‑score (in number of bars)
    lookback: dict = None

    def __post_init__(self):
        if self.timeframes is None:
            self.timeframes = ['M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
        if self.weights is None:
            self.weights = {
                'M15': 0.10,
                'H1':  0.15,
                'H4':  0.25,
                'D1':  0.30,
                'W1':  0.12,
                'MN1': 0.08,
            }
        if self.lookback is None:
            self.lookback = {
                'M15': 60,
                'H1':  60,
                'H4':  60,
                'D1':  60,
                'W1':  60,
                'MN1': 60,
            }

config = StrengthConfig()
