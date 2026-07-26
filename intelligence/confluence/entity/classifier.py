"""
Phase 4: Global Entity Intelligence - Entity Classifier

Classifies entities by type for proper processing.
"""

from ..contracts import EntityType


class EntityClassifier:
    """
    Classifies entities by type.

    Determines whether an entity is a currency, index, commodity,
    bond, rate, or other type.
    """

    # Currency symbols
    CURRENCY_SYMBOLS = {
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
        "HKD",
        "TRY",
        "ZAR",
        "BRL",
        "RUB",
    }

    # Index symbols
    INDEX_SYMBOLS = {
        "US500",
        "SPX",
        "S&P500",
        "US100",
        "NAS100",
        "NDX",
        "US30",
        "DJI",
        "DOW",
        "GER40",
        "DAX",
        "UK100",
        "FTSE",
        "FRA40",
        "CAC40",
        "JP225",
        "NIKKEI",
        "HK50",
        "HSI",
        "AU200",
        "ASX200",
        "CHINA50",
        "SHANGHAI",
    }

    # Commodity symbols
    COMMODITY_SYMBOLS = {
        "XAUUSD",
        "XAGUSD",
        "CL=F",
        "BZ=F",
        "COPPER",
        "NATURAL_GAS",
        "GOLD",
        "SILVER",
        "OIL",
        "BRENT",
        "WTI",
        "NG",
    }

    # Bond/Rate symbols
    BOND_SYMBOLS = {
        "US10Y",
        "US02Y",
        "US30Y",
        "DE10Y",
        "DE02Y",
        "GB10Y",
        "JP10Y",
        "CH10Y",
        "AU10Y",
        "CA10Y",
    }

    # Symbol to entity type mapping
    SYMBOL_TO_TYPE: dict[str, EntityType] = {}

    @classmethod
    def _build_map(cls) -> None:
        """Build the symbol-to-type mapping."""
        if cls.SYMBOL_TO_TYPE:
            return

        for symbol in cls.CURRENCY_SYMBOLS:
            cls.SYMBOL_TO_TYPE[symbol] = EntityType.CURRENCY

        for symbol in cls.INDEX_SYMBOLS:
            cls.SYMBOL_TO_TYPE[symbol] = EntityType.INDEX

        for symbol in cls.COMMODITY_SYMBOLS:
            cls.SYMBOL_TO_TYPE[symbol] = EntityType.COMMODITY

        for symbol in cls.BOND_SYMBOLS:
            cls.SYMBOL_TO_TYPE[symbol] = EntityType.BOND

    @classmethod
    def classify(cls, entity: str) -> EntityType:
        """
        Classify an entity by symbol.

        Args:
            entity: Entity symbol (e.g., "USD", "EUR", "XAUUSD")

        Returns:
            EntityType: The classified entity type
        """
        cls._build_map()

        # Exact match
        if entity in cls.SYMBOL_TO_TYPE:
            return cls.SYMBOL_TO_TYPE[entity]

        # Check if it's a currency pair (e.g., "AUDUSD")
        # In this case, both are currencies
        # The rating engine will handle this specially
        if len(entity) == 6 and entity.isupper() and all(c.isalpha() for c in entity):
            # Could be a currency pair
            # Return CURRENCY for now, the aggregator will handle pairs
            return EntityType.CURRENCY

        # Default to unknown - treat as asset
        return EntityType.ASSET_CLASS

    @classmethod
    def is_currency(cls, entity: str) -> bool:
        """Check if entity is a currency."""
        return cls.classify(entity) == EntityType.CURRENCY

    @classmethod
    def is_index(cls, entity: str) -> bool:
        """Check if entity is an index."""
        return cls.classify(entity) == EntityType.INDEX

    @classmethod
    def is_commodity(cls, entity: str) -> bool:
        """Check if entity is a commodity."""
        return cls.classify(entity) == EntityType.COMMODITY

    @classmethod
    def is_bond(cls, entity: str) -> bool:
        """Check if entity is a bond/rate."""
        return cls.classify(entity) == EntityType.BOND

    @classmethod
    def is_currency_pair(cls, entity: str) -> bool:
        """Check if entity is a currency pair (e.g., AUDUSD)."""
        return (
            len(entity) == 6 and entity.isupper() and all(c.isalpha() for c in entity)
        )

    @classmethod
    def get_currency_type(cls) -> EntityType:
        """Get the currency entity type."""
        return EntityType.CURRENCY

    @classmethod
    def get_entity_types(cls) -> list:
        """Get all entity types."""
        return [
            EntityType.CURRENCY,
            EntityType.INDEX,
            EntityType.COMMODITY,
            EntityType.BOND,
            EntityType.RATE,
            EntityType.ASSET_CLASS,
            EntityType.REGIME,
        ]
