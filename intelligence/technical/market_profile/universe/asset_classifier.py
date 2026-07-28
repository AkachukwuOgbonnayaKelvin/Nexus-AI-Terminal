"""
Asset Classifier – maps symbols to asset classes and groups.
"""

from ..enums import AssetClass
from .asset_registry import AssetRegistry

# Default mapping for common symbols – extend as needed.
DEFAULT_CLASS_MAP = {
    # FX Majors
    "EURUSD": AssetClass.FX.value,
    "GBPUSD": AssetClass.FX.value,
    "USDJPY": AssetClass.FX.value,
    "AUDUSD": AssetClass.FX.value,
    "USDCAD": AssetClass.FX.value,
    "USDCHF": AssetClass.FX.value,
    "NZDUSD": AssetClass.FX.value,
    # FX Minors
    "EURGBP": AssetClass.FX.value,
    "EURJPY": AssetClass.FX.value,
    "EURCHF": AssetClass.FX.value,
    "EURNZD": AssetClass.FX.value,
    "EURCAD": AssetClass.FX.value,
    "GBPAUD": AssetClass.FX.value,
    "GBPJPY": AssetClass.FX.value,
    "GBPCAD": AssetClass.FX.value,
    "GBPCHF": AssetClass.FX.value,
    "GBPNZD": AssetClass.FX.value,
    "AUDCAD": AssetClass.FX.value,
    "AUDJPY": AssetClass.FX.value,
    "AUDNZD": AssetClass.FX.value,
    "CADJPY": AssetClass.FX.value,
    "CADCHF": AssetClass.FX.value,
    "CHFJPY": AssetClass.FX.value,
    "NZDCAD": AssetClass.FX.value,
    "NZDJPY": AssetClass.FX.value,
    # Indices
    "US500": AssetClass.INDEX.value,
    "US30": AssetClass.INDEX.value,
    "US100": AssetClass.INDEX.value,
    "NAS100": AssetClass.INDEX.value,
    "GER40": AssetClass.INDEX.value,
    "UK100": AssetClass.INDEX.value,
    "FRA40": AssetClass.INDEX.value,
    "HK50": AssetClass.INDEX.value,
    "JP225": AssetClass.INDEX.value,
    "AU200": AssetClass.INDEX.value,
    # Commodities
    "XAUUSD": AssetClass.COMMODITY.value,
    "XAGUSD": AssetClass.COMMODITY.value,
    "CL=F": AssetClass.COMMODITY.value,
    "BZ=F": AssetClass.COMMODITY.value,
    "NG=F": AssetClass.COMMODITY.value,
    "Copper": AssetClass.COMMODITY.value,
    "SpotBrent": AssetClass.COMMODITY.value,
    # Crypto
    "BTCUSD": AssetClass.CRYPTO.value,
    "ETHUSD": AssetClass.CRYPTO.value,
    "ADAUSD": AssetClass.CRYPTO.value,
    "DOTUSD": AssetClass.CRYPTO.value,
    "SOLUSD": AssetClass.CRYPTO.value,
    "LINKUSD": AssetClass.CRYPTO.value,
}

DEFAULT_GROUP_MAP = {
    "EURUSD": "EUR",
    "GBPUSD": "GBP",
    "USDJPY": "USD",
    "AUDUSD": "AUD",
    "USDCAD": "USD",
    "USDCHF": "USD",
    "NZDUSD": "NZD",
    "EURGBP": "EUR",
    "EURJPY": "EUR",
    "EURCHF": "EUR",
    "EURNZD": "EUR",
    "EURCAD": "EUR",
    "GBPAUD": "GBP",
    "GBPJPY": "GBP",
    "GBPCAD": "GBP",
    "GBPCHF": "GBP",
    "GBPNZD": "GBP",
    "AUDCAD": "AUD",
    "AUDJPY": "AUD",
    "AUDNZD": "AUD",
    "CADJPY": "CAD",
    "CADCHF": "CAD",
    "CHFJPY": "CHF",
    "NZDCAD": "NZD",
    "NZDJPY": "NZD",
    "US500": "US",
    "US30": "US",
    "US100": "US",
    "NAS100": "US",
    "GER40": "Europe",
    "UK100": "Europe",
    "FRA40": "Europe",
    "HK50": "Asia",
    "JP225": "Asia",
    "AU200": "Australia",
    "XAUUSD": "Precious",
    "XAGUSD": "Precious",
    "CL=F": "Energy",
    "BZ=F": "Energy",
    "NG=F": "Energy",
    "Copper": "Base",
    "SpotBrent": "Energy",
    "BTCUSD": "BTC",
    "ETHUSD": "ETH",
    "ADAUSD": "Alt",
    "DOTUSD": "Alt",
    "SOLUSD": "Alt",
    "LINKUSD": "Alt",
}


def create_default_registry(symbols: list[str]) -> AssetRegistry:
    """Create an AssetRegistry with default class/group mappings."""
    class_map = {s: DEFAULT_CLASS_MAP.get(s, AssetClass.UNKNOWN.value) for s in symbols}
    group_map = {s: DEFAULT_GROUP_MAP.get(s, "unknown") for s in symbols}
    return AssetRegistry(symbols, class_map, group_map)
