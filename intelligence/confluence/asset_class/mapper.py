"""
Phase 5: Asset-Class Intelligence - Asset-Class Mapper

Maps entities to their asset classes.
"""

from typing import Dict, List, Optional

from ..contracts import GlobalEntityRating, AssetClass


class AssetClassMapper:
    """
    Maps entities to asset classes.

    Asset Classes:
    - FX: Currencies
    - METALS: Gold, Silver, Copper
    - EQUITIES: Stock indices
    - BONDS: Government bonds
    - ENERGY: Oil, Gas
    - COMMODITIES: Broader commodities
    """

    # Entity to Asset Class mapping
    ENTITY_TO_ASSET_CLASS: Dict[str, AssetClass] = {}

    # Currency mapping
    CURRENCY_LIST = [
        "USD",
        "EUR",
        "GBP",
        "JPY",
        "CHF",
        "CAD",
        "AUD",
        "NZD",
        "SEK",
        "NOK",
        "DKK",
        "MXN",
        "CNY",
        "INR",
        "KRW",
        "SGD",
    ]

    # Metals mapping
    METALS_LIST = ["XAUUSD", "XAGUSD", "COPPER", "PLATINUM", "PALLADIUM"]

    # Equities mapping
    EQUITIES_LIST = [
        "US500",
        "US100",
        "US30",
        "GER40",
        "UK100",
        "FRA40",
        "JP225",
        "HK50",
        "AU200",
        "CHINA50",
        "S&P500",
        "NASDAQ",
        "DOW",
        "DAX",
        "FTSE",
        "CAC40",
        "NIKKEI",
    ]

    # Bonds mapping
    BONDS_LIST = [
        "US10Y",
        "US02Y",
        "US30Y",
        "DE10Y",
        "DE02Y",
        "GB10Y",
        "JP10Y",
        "CH10Y",
    ]

    # Energy mapping
    ENERGY_LIST = ["CL=F", "BZ=F", "NG=F", "WTI", "BRENT", "NATURAL_GAS"]

    @classmethod
    def _build_map(cls) -> None:
        """Build the entity-to-asset-class mapping."""
        if cls.ENTITY_TO_ASSET_CLASS:
            return

        for entity in cls.CURRENCY_LIST:
            cls.ENTITY_TO_ASSET_CLASS[entity] = AssetClass.FX

        for entity in cls.METALS_LIST:
            cls.ENTITY_TO_ASSET_CLASS[entity] = AssetClass.METALS

        for entity in cls.EQUITIES_LIST:
            cls.ENTITY_TO_ASSET_CLASS[entity] = AssetClass.EQUITIES

        for entity in cls.BONDS_LIST:
            cls.ENTITY_TO_ASSET_CLASS[entity] = AssetClass.BONDS

        for entity in cls.ENERGY_LIST:
            cls.ENTITY_TO_ASSET_CLASS[entity] = AssetClass.ENERGY

    @classmethod
    def map_entity(cls, entity: str) -> Optional[AssetClass]:
        """
        Map a single entity to its asset class.

        Args:
            entity: Entity symbol (e.g., "USD", "XAUUSD")

        Returns:
            AssetClass: The asset class, or None if unknown
        """
        cls._build_map()
        return cls.ENTITY_TO_ASSET_CLASS.get(entity)

    @classmethod
    def map_rating(cls, rating: GlobalEntityRating) -> Optional[AssetClass]:
        """
        Map a rating's entity to its asset class.

        Args:
            rating: GlobalEntityRating

        Returns:
            AssetClass: The asset class, or None if unknown
        """
        return cls.map_entity(rating.entity)

    @classmethod
    def map_ratings(
        cls, ratings: List[GlobalEntityRating]
    ) -> Dict[AssetClass, List[GlobalEntityRating]]:
        """
        Map multiple ratings to asset classes.

        Args:
            ratings: List of GlobalEntityRating

        Returns:
            Dict mapping AssetClass to list of ratings
        """
        cls._build_map()

        grouped: Dict[AssetClass, List[GlobalEntityRating]] = {}

        for rating in ratings:
            asset_class = cls.map_entity(rating.entity)
            if asset_class is not None:
                if asset_class not in grouped:
                    grouped[asset_class] = []
                grouped[asset_class].append(rating)

        return grouped

    @classmethod
    def get_asset_classes(cls) -> List[AssetClass]:
        """Get all supported asset classes."""
        return [
            AssetClass.FX,
            AssetClass.METALS,
            AssetClass.EQUITIES,
            AssetClass.BONDS,
            AssetClass.ENERGY,
            AssetClass.COMMODITIES,
        ]

    @classmethod
    def get_asset_class_name(cls, asset_class: AssetClass) -> str:
        """Get human-readable name for an asset class."""
        names = {
            AssetClass.FX: "FX",
            AssetClass.METALS: "Metals",
            AssetClass.EQUITIES: "Equities",
            AssetClass.BONDS: "Bonds",
            AssetClass.ENERGY: "Energy",
            AssetClass.COMMODITIES: "Commodities",
            AssetClass.GOLD: "Gold",
            AssetClass.SILVER: "Silver",
            AssetClass.CRYPTO: "Crypto",
        }
        return names.get(asset_class, asset_class.value)

    @classmethod
    def get_entities_for_class(cls, asset_class: AssetClass) -> List[str]:
        """Get all entities that belong to an asset class."""
        cls._build_map()
        return [e for e, ac in cls.ENTITY_TO_ASSET_CLASS.items() if ac == asset_class]
