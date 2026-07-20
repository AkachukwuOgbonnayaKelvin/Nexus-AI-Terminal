# -*- coding: utf-8 -*-
"""Provider Diagnostics - Detailed provider status per symbol"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from corporate_earnings_engine.providers.router import ProviderRouter


class ProviderDiagnostics:
    """Provides detailed diagnostics for each symbol/provider"""
    
    def __init__(self):
        self.router = ProviderRouter()
    
    def diagnose_symbol(self, symbol: str) -> Dict[str, Any]:
        """Get detailed diagnostics for a symbol"""
        
        result = {
            "symbol": symbol,
            "exchange": self.router.get_exchange_for_symbol(symbol),
            "providers": [],
            "overall_status": "UNKNOWN"
        }
        
        providers = self.router.get_providers_for_symbol(symbol)
        
        for provider in providers:
            provider_result = {
                "name": provider.get_provider_name(),
                "tier": provider.get_tier(),
                "available": provider.is_available(),
                "data_found": False,
                "records": 0,
                "error": None
            }
            
            try:
                data = provider.get_earnings(symbol)
                if data:
                    provider_result["data_found"] = True
                    provider_result["records"] = len(data)
                    provider_result["latest"] = {
                        "period": data[0].period,
                        "eps": data[0].actual_eps
                    }
            except Exception as e:
                provider_result["error"] = str(e)
            
            result["providers"].append(provider_result)
        
        # Determine overall status
        if any(p["data_found"] for p in result["providers"]):
            result["overall_status"] = "SUCCESS"
        elif any(p["available"] for p in result["providers"]):
            result["overall_status"] = "AVAILABLE_NO_DATA"
        else:
            result["overall_status"] = "UNAVAILABLE"
        
        return result
    
    def diagnose_regions(self, symbols: Dict[str, List[str]]) -> Dict[str, Any]:
        """Diagnose multiple regions"""
        
        results = {}
        for region, region_symbols in symbols.items():
            results[region] = {}
            for symbol in region_symbols:
                results[region][symbol] = self.diagnose_symbol(symbol)
        
        return results
