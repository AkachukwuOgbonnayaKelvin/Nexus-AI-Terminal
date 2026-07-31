"""
Asset Synchronizer Configuration
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class SyncConfig:
    """Configuration for synchronizer."""

    core_host: str = os.getenv('CORE_DB_HOST', 'localhost')
    core_port: int = int(os.getenv('CORE_DB_PORT', 5432))
    core_dbname: str = os.getenv('CORE_DB_NAME', 'nexus_core')
    core_user: str = os.getenv('CORE_DB_USER', 'postgres')
    core_password: str = os.getenv('CORE_DB_PASSWORD', '6468')

    asset_host: str = os.getenv('ASSET_DB_HOST', 'localhost')
    asset_port: int = int(os.getenv('ASSET_DB_PORT', 5432))
    asset_dbname: str = os.getenv('ASSET_DB_NAME', 'nexus_asset')
    asset_user: str = os.getenv('ASSET_DB_USER', 'postgres')
    asset_password: str = os.getenv('ASSET_DB_PASSWORD', '6468')

    batch_size: int = int(os.getenv('SYNC_BATCH_SIZE', 10000))
    sync_interval_seconds: int = int(os.getenv('SYNC_INTERVAL', 5))

    tables_to_sync: list = None

    def __post_init__(self):
        if self.tables_to_sync is None:
            self.tables_to_sync = ['prices', 'calendar_events', 'symbols']


config = SyncConfig()
