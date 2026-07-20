# -*- coding: utf-8 -*-
"""Provider Registry - Manages earnings providers with hierarchy"""

from typing import Dict, List, Optional, Any
from enum import IntEnum
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from corporate_earnings_engine.providers.base import EarningsProvider
from corporate_earnings_engine.providers.primary.sec_edgar.provider import SECEdgarProvider
from corporate_earnings_engine.providers.secondary.financial_modeling_prep.provider import FMPProvider


class ProviderTier(IntEnum):
    TIER_1_PRIMARY = 1
    TIER_2_SECONDARY = 2


class ProviderRegistry:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.providers: Dict[str, EarningsProvider] = {}
        self.tiers: Dict[str, ProviderTier] = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        # Tier 1: Primary sources
        self.providers["sec_edgar"] = SECEdgarProvider(self.config.get("sec_edgar", {}))
        self.tiers["sec_edgar"] = ProviderTier.TIER_1_PRIMARY
        
        # Tier 2: Secondary sources
        self.providers["financial_modeling_prep"] = FMPProvider(self.config.get("financial_modeling_prep", {}))
        self.tiers["financial_modeling_prep"] = ProviderTier.TIER_2_SECONDARY
    
    def get_primary_provider(self) -> Optional[EarningsProvider]:
        for name, provider in self.providers.items():
            if self.tiers.get(name) == ProviderTier.TIER_1_PRIMARY:
                if provider.is_available():
                    return provider
        return None
    
    def get_providers_by_tier(self, tier: int) -> List[EarningsProvider]:
        return [p for n, p in self.providers.items() if self.tiers.get(n) == ProviderTier(tier)]
    
    def get_health_status(self) -> Dict[str, Any]:
        status = {}
        for name, provider in self.providers.items():
            health = provider.get_health()
            health["tier"] = self.tiers.get(name, ProviderTier.TIER_2_SECONDARY).value
            status[name] = health
        return status
