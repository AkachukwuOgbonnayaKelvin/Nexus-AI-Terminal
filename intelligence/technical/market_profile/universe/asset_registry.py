"""
Asset Registry – maintains the list of all symbols to scan.
"""


class AssetRegistry:
    """
    Provides the list of symbols and their metadata (class, group).
    In production, this could be loaded from a database or config file.
    """

    def __init__(
        self,
        symbols: list[str],
        asset_class_map: dict[str, str],
        group_map: dict[str, str],
    ):
        """
        Args:
            symbols: list of symbol strings (e.g., ["EURUSD", "GBPUSD", ...])
            asset_class_map: dict mapping symbol -> asset class (e.g., "EURUSD" -> "fx")
            group_map: dict mapping symbol -> group (e.g., "EURUSD" -> "EUR")
        """
        self.symbols = symbols
        self.asset_class_map = asset_class_map
        self.group_map = group_map

    def get_all_symbols(self) -> list[str]:
        return self.symbols

    def get_asset_class(self, symbol: str) -> str:
        return self.asset_class_map.get(symbol, "unknown")

    def get_group(self, symbol: str) -> str:
        return self.group_map.get(symbol, "unknown")

    def get_all_metadata(self) -> list[dict[str, str]]:
        return [
            {"symbol": s, "class": self.get_asset_class(s), "group": self.get_group(s)}
            for s in self.symbols
        ]
