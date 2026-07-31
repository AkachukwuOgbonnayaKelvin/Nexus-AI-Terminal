import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class CompositeConfig:
    asset_host: str = os.getenv('ASSET_DB_HOST', 'localhost')
    asset_port: int = int(os.getenv('ASSET_DB_PORT', 5432))
    asset_dbname: str = os.getenv('ASSET_DB_NAME', 'nexus_asset')
    asset_user: str = os.getenv('ASSET_DB_USER', 'postgres')
    asset_password: str = os.getenv('ASSET_DB_PASSWORD', '6468')

    weights: dict = None

    def __post_init__(self):
        if self.weights is None:
            self.weights = {
                'technical': 0.35,
                'macro': 0.15,
                'micro': 0.0,
                'monetary': 0.20,
                'intermarket': 0.15,
                'risk': 0.10,
                'cot': 0.05
            }

config = CompositeConfig()
