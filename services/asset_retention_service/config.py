import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class RetentionConfig:
    # Asset database connection
    asset_host: str = os.getenv('ASSET_DB_HOST', 'localhost')
    asset_port: int = int(os.getenv('ASSET_DB_PORT', 5432))
    asset_dbname: str = os.getenv('ASSET_DB_NAME', 'nexus_asset')
    asset_user: str = os.getenv('ASSET_DB_USER', 'postgres')
    asset_password: str = os.getenv('ASSET_DB_PASSWORD', '6468')

    # Retention periods in days for each timeframe
    retention_policy: dict = None

    def __post_init__(self):
        if self.retention_policy is None:
            self.retention_policy = {
                'M5': 180,
                'M15': 365,
                'H1': 730,
                'H4': 1095,
                'D1': 3650,
                'W1': 5475,
                'MN1': 7300,
            }

config = RetentionConfig()
