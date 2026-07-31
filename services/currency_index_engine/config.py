import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class IndexConfig:
    asset_host: str = os.getenv('ASSET_DB_HOST', 'localhost')
    asset_port: int = int(os.getenv('ASSET_DB_PORT', 5432))
    asset_dbname: str = os.getenv('ASSET_DB_NAME', 'nexus_asset')
    asset_user: str = os.getenv('ASSET_DB_USER', 'postgres')
    asset_password: str = os.getenv('ASSET_DB_PASSWORD', '6468')

    # Timeframe configuration: lookback, minimum bars, role, weight
    timeframe_config: dict = None

    # Data status weight multiplier
    data_status_weight: dict = None

    # Fallback chain: requested -> list of fallbacks in order
    fallback_chain: dict = None

    # Composite definitions (group names -> list of timeframes)
    composites: dict = None

    # Weights for overall composite (Strategic, Swing, Tactical)
    overall_weights: dict = None

    def __post_init__(self):
        if self.timeframe_config is None:
            self.timeframe_config = {
                "MN1": {"lookback": 60, "minimum_bars": 20, "role": "strategic", "weight": 0.10},
                "W1":  {"lookback": 60, "minimum_bars": 30, "role": "strategic", "weight": 0.25},
                "D1":  {"lookback": 60, "minimum_bars": 60, "role": "strategic", "weight": 0.35},
                "H4":  {"lookback": 60, "minimum_bars": 100, "role": "swing", "weight": 0.30},
                "H1":  {"lookback": 60, "minimum_bars": 100, "role": "tactical", "weight": 0.35},
                "M30": {"lookback": 60, "minimum_bars": 150, "role": "tactical", "weight": 0.20},
                "M15": {"lookback": 60, "minimum_bars": 200, "role": "tactical", "weight": 0.15},
                "M5":  {"lookback": 60, "minimum_bars": 300, "role": "tactical", "weight": 0.10},
            }

        if self.data_status_weight is None:
            self.data_status_weight = {
                "VALID": 1.0,
                "FALLBACK": 0.55,
                "NO_DATA": 0.0,
                "INSUFFICIENT": 0.0,
            }

        if self.fallback_chain is None:
            self.fallback_chain = {
                "M5":  ["M15", "M30", "H1"],
                "M15": ["M30", "H1", "H4"],
                "M30": ["H1", "H4", "D1"],
                "H1":  ["H4", "D1", "W1"],
                "H4":  ["D1", "W1", "MN1"],
                "D1":  ["W1", "MN1"],
                "W1":  ["MN1"],
                "MN1": [],
            }

        if self.composites is None:
            self.composites = {
                "STRATEGIC": ["MN1", "W1", "D1"],
                "SWING": ["H4"],
                "TACTICAL": ["H1", "M30", "M15", "M5"],
            }

        if self.overall_weights is None:
            self.overall_weights = {
                "STRATEGIC": 0.45,
                "SWING": 0.35,
                "TACTICAL": 0.20,
            }

config = IndexConfig()
