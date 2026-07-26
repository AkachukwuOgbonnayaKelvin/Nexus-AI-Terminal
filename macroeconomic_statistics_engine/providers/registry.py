"""Provider Registry - Manages macroeconomic data providers with hierarchy"""

import sys
from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from macroeconomic_statistics_engine.providers.base import MacroProvider
from macroeconomic_statistics_engine.providers.official.fred import FREDProvider
from macroeconomic_statistics_engine.providers.official.world_bank import (
    WorldBankProvider,
)


class ProviderTier(IntEnum):
    """Provider tier hierarchy"""

    TIER_1_PRIMARY = 1  # Official national sources
    TIER_2_SECONDARY = 2  # International official sources
    TIER_3_FALLBACK = 3  # Commercial aggregators


class MacroProviderRegistry:
    """Registry for macroeconomic providers with priority hierarchy"""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.providers: dict[str, MacroProvider] = {}
        self.tiers: dict[str, ProviderTier] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all providers with their tiers"""

        # Tier 1: Primary official sources
        self.providers["fred"] = FREDProvider(self.config.get("fred", {}))
        self.tiers["fred"] = ProviderTier.TIER_1_PRIMARY
        print("[REGISTRY] FRED registered as TIER 1 PRIMARY")

        # Tier 2: International official sources
        self.providers["world_bank"] = WorldBankProvider(
            self.config.get("world_bank", {})
        )
        self.tiers["world_bank"] = ProviderTier.TIER_2_SECONDARY
        print("[REGISTRY] World Bank registered as TIER 2 SECONDARY")

        # Tier 3: Commercial aggregators (to be added)
        # self.providers["trading_economics"] = TradingEconomicsProvider(...)
        # self.tiers["trading_economics"] = ProviderTier.TIER_3_FALLBACK

    def get_provider(self, name: str) -> MacroProvider | None:
        """Get a provider by name"""
        return self.providers.get(name)

    def get_primary_provider(
        self, indicator: str, country: str
    ) -> MacroProvider | None:
        """Get the primary provider for an indicator/country"""
        # FRED for US data
        if country == "US":
            provider = self.providers.get("fred")
            if provider and provider.is_available():
                return provider
        return None

    def get_providers_for_indicator(
        self, indicator: str, country: str
    ) -> list[MacroProvider]:
        """Get all providers that can supply an indicator, ordered by tier"""
        providers = []

        # Tier 1: Primary
        if country == "US":
            fred = self.providers.get("fred")
            if fred and fred.is_available():
                indicators = fred.get_available_indicators(country)
                if indicator in indicators:
                    providers.append(fred)

        # Tier 2: International (World Bank covers all countries)
        world_bank = self.providers.get("world_bank")
        if world_bank and world_bank.is_available():
            indicators = world_bank.get_available_indicators(country)
            if indicator in indicators:
                providers.append(world_bank)

        # Tier 3: Fallback
        # To be added

        return providers

    def get_indicator_with_failover(
        self,
        indicator: str,
        country: str,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[Any]:
        """Get indicator data with automatic failover"""

        # Try Tier 1 providers first
        tier1_providers = self._get_providers_by_tier(ProviderTier.TIER_1_PRIMARY)
        for provider in tier1_providers:
            if provider.is_available():
                data = provider.get_indicator(indicator, country, start_date, end_date)
                if data:
                    return data

        # Try Tier 2 providers
        tier2_providers = self._get_providers_by_tier(ProviderTier.TIER_2_SECONDARY)
        for provider in tier2_providers:
            if provider.is_available():
                data = provider.get_indicator(indicator, country, start_date, end_date)
                if data:
                    return data

        # Try Tier 3 providers
        tier3_providers = self._get_providers_by_tier(ProviderTier.TIER_3_FALLBACK)
        for provider in tier3_providers:
            if provider.is_available():
                data = provider.get_indicator(indicator, country, start_date, end_date)
                if data:
                    return data

        return []

    def _get_providers_by_tier(self, tier: ProviderTier) -> list[MacroProvider]:
        """Get all providers of a specific tier"""
        return [p for name, p in self.providers.items() if self.tiers.get(name) == tier]

    def get_health_status(self) -> dict[str, Any]:
        """Get health status of all providers"""
        status = {}
        for name, provider in self.providers.items():
            health = provider.get_health()
            health["tier"] = self.tiers.get(name, ProviderTier.TIER_3_FALLBACK).value
            status[name] = health
        return status
