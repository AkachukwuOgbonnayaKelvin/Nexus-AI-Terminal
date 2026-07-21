# -*- coding: utf-8 -*-
"""Provider Registry - Manages earnings providers with hierarchy"""

from typing import Dict, List, Optional, Any
from enum import IntEnum
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from corporate_earnings_engine.providers.base import EarningsProvider
from corporate_earnings_engine.providers.primary.sec_edgar.provider import (
    SECEdgarProvider,
)
from corporate_earnings_engine.providers.secondary.financial_modeling_prep.provider import (
    FMPProvider,
)
from corporate_earnings_engine.providers.secondary.finnhub.provider import (
    FinnhubProvider,
)
from corporate_earnings_engine.providers.tertiary.yahoo_provider import (
    YahooFinanceProvider,
)


class ProviderTier(IntEnum):
    TIER_1_PRIMARY = 1
    TIER_2_SECONDARY = 2
    TIER_3_FALLBACK = 3


class ProviderRegistry:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.providers: Dict[str, EarningsProvider] = {}
        self.tiers: Dict[str, ProviderTier] = {}
        self._load_from_env()
        self._initialize_providers()
        self._print_status()

    def _load_from_env(self):
        """Load API keys from environment variables"""
        finnhub_key = os.getenv("FINNHUB_API_KEY", "")
        if finnhub_key:
            self.config["finnhub"] = {"api_key": finnhub_key}
            print("[REGISTRY] Loaded Finnhub API key")
        else:
            print("[REGISTRY] No Finnhub API key found")

        fmp_key = os.getenv("FMP_API_KEY", "")
        if fmp_key:
            self.config["financial_modeling_prep"] = {"api_key": fmp_key}
            print("[REGISTRY] Loaded FMP API key")
        else:
            print("[REGISTRY] No FMP API key found")

    def _initialize_providers(self):
        # Tier 1: Primary sources
        self.providers["sec_edgar"] = SECEdgarProvider(self.config.get("sec_edgar", {}))
        self.tiers["sec_edgar"] = ProviderTier.TIER_1_PRIMARY
        print("[REGISTRY] SEC EDGAR registered as TIER 1 PRIMARY")

        # Tier 2: Secondary sources
        self.providers["financial_modeling_prep"] = FMPProvider(
            self.config.get("financial_modeling_prep", {})
        )
        self.tiers["financial_modeling_prep"] = ProviderTier.TIER_2_SECONDARY
        print("[REGISTRY] Financial Modeling Prep registered as TIER 2 SECONDARY")

        self.providers["finnhub"] = FinnhubProvider(self.config.get("finnhub", {}))
        self.tiers["finnhub"] = ProviderTier.TIER_2_SECONDARY
        print("[REGISTRY] Finnhub registered as TIER 2 SECONDARY")

        # Tier 3: Fallback sources
        self.providers["yahoo_finance"] = YahooFinanceProvider(
            self.config.get("yahoo_finance", {})
        )
        self.tiers["yahoo_finance"] = ProviderTier.TIER_3_FALLBACK
        print("[REGISTRY] Yahoo Finance registered as TIER 3 FALLBACK")

    def _print_status(self):
        """Print provider status"""
        print("\n[REGISTRY] Provider Status:")
        for name, provider in self.providers.items():
            available = provider.is_available()
            tier = self.tiers.get(name, ProviderTier.TIER_3_FALLBACK).value
            print(f"  {name}: Tier {tier}, Available: {available}")

    def get_provider(self, name: str) -> Optional[EarningsProvider]:
        return self.providers.get(name)

    def get_primary_provider(self) -> Optional[EarningsProvider]:
        for name, provider in self.providers.items():
            if self.tiers.get(name) == ProviderTier.TIER_1_PRIMARY:
                if provider.is_available():
                    return provider
        return None

    def get_providers_by_tier(self, tier: int) -> List[EarningsProvider]:
        return [
            p
            for n, p in self.providers.items()
            if self.tiers.get(n) == ProviderTier(tier)
        ]

    def get_all_providers(self) -> List[EarningsProvider]:
        return list(self.providers.values())

    def get_health_status(self) -> Dict[str, Any]:
        status = {}
        for name, provider in self.providers.items():
            health = provider.get_health()
            health["tier"] = self.tiers.get(name, ProviderTier.TIER_3_FALLBACK).value
            status[name] = health
        return status
