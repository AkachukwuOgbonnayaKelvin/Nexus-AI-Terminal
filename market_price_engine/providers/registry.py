# -*- coding: utf-8 -*-
"""Provider Registry - Manages all market data providers with priority hierarchy"""

from typing import Dict, List, Optional, Any
from enum import Enum
import os
import yaml
from pathlib import Path

from providers.base import MarketDataProvider
from providers.mt5.provider import MT5Provider
from providers.yahoo.provider import YahooFinanceProvider
from providers.alpha_vantage.provider import AlphaVantageProvider


class ProviderPriority(Enum):
    PRIMARY = 1
    SECONDARY = 2
    TERTIARY = 3
    BACKUP = 4


class ProviderRegistry:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.providers: Dict[str, MarketDataProvider] = {}
        self.priorities: Dict[str, ProviderPriority] = {}
        self._load_mt5_config()
        self._initialize_providers()

    def _load_mt5_config(self):
        """Load MT5 configuration from file or environment"""
        # Default Pepperstone MT5 path
        default_config = {
            "terminal_path": "C:/Program Files/Pepperstone MetaTrader 5/terminal64.exe",
            "login": 51492515,
            "password": "mumILOVEU@12",
            "server": "PepperstoneBS-MT5-Live01",
        }

        # Try to load from config file
        config_path = Path(__file__).parent.parent / "config" / "mt5_config.yaml"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    mt5_config = yaml.safe_load(f).get("mt5", {})
                    self.config["mt5"] = {**default_config, **mt5_config}
                    print("[REGISTRY] Loaded MT5 config from file")
            except Exception as e:
                print(f"[REGISTRY] Error loading MT5 config: {e}")
                self.config["mt5"] = default_config
        else:
            # Use default config
            self.config["mt5"] = default_config
            print("[REGISTRY] Using default MT5 config")

        # Override with environment variables if set
        if os.getenv("MT5_LOGIN"):
            self.config["mt5"]["login"] = int(os.getenv("MT5_LOGIN"))
        if os.getenv("MT5_PASSWORD"):
            self.config["mt5"]["password"] = os.getenv("MT5_PASSWORD")
        if os.getenv("MT5_SERVER"):
            self.config["mt5"]["server"] = os.getenv("MT5_SERVER")
        if os.getenv("MT5_TERMINAL_PATH"):
            self.config["mt5"]["terminal_path"] = os.getenv("MT5_TERMINAL_PATH")

    def _initialize_providers(self):
        """Initialize all configured providers with priorities"""

        # 1. MT5 Provider (PRIMARY - Pepperstone)
        mt5_config = self.config.get("mt5", {})
        self.providers["mt5"] = MT5Provider(mt5_config)
        self.priorities["mt5"] = ProviderPriority.PRIMARY
        print(
            f"[REGISTRY] MT5 PRIMARY - Terminal: {mt5_config.get('terminal_path', 'default')}"
        )

        # 2. Yahoo Finance Provider (SECONDARY)
        yahoo_config = self.config.get("yahoo", {})
        self.providers["yahoo"] = YahooFinanceProvider(yahoo_config)
        self.priorities["yahoo"] = ProviderPriority.SECONDARY
        print("[REGISTRY] Yahoo Finance SECONDARY")

        # 3. Alpha Vantage Provider (TERTIARY)
        alpha_config = self.config.get("alpha_vantage", {})
        self.providers["alpha_vantage"] = AlphaVantageProvider(alpha_config)
        self.priorities["alpha_vantage"] = ProviderPriority.TERTIARY
        print("[REGISTRY] Alpha Vantage TERTIARY")

    def get_provider(self, name: str) -> Optional[MarketDataProvider]:
        return self.providers.get(name)

    def get_primary_provider(self) -> Optional[MarketDataProvider]:
        provider = self.providers.get("mt5")
        if provider and provider.is_available():
            print("[REGISTRY] Using MT5 primary")
            return provider
        print("[REGISTRY] MT5 unavailable, falling back to secondary")
        return self.get_secondary_provider()

    def get_secondary_provider(self) -> Optional[MarketDataProvider]:
        provider = self.providers.get("yahoo")
        if provider and provider.is_available():
            return provider
        return self.get_tertiary_provider()

    def get_tertiary_provider(self) -> Optional[MarketDataProvider]:
        provider = self.providers.get("alpha_vantage")
        if provider and provider.is_available():
            return provider
        return None

    def get_priority_order(self) -> List[str]:
        priority_map = {
            ProviderPriority.PRIMARY: 0,
            ProviderPriority.SECONDARY: 1,
            ProviderPriority.TERTIARY: 2,
            ProviderPriority.BACKUP: 3,
        }
        return sorted(
            self.providers.keys(),
            key=lambda x: priority_map.get(
                self.priorities.get(x, ProviderPriority.BACKUP), 4
            ),
        )

    def get_health_status(self) -> Dict[str, Any]:
        status = {}
        for name, provider in self.providers.items():
            health = provider.get_health()
            health["priority"] = self.priorities.get(
                name, ProviderPriority.BACKUP
            ).value
            status[name] = health
        return status

    def get_best_available_provider(self) -> Optional[MarketDataProvider]:
        for name in self.get_priority_order():
            provider = self.providers.get(name)
            if provider and provider.is_available():
                return provider
        return None
