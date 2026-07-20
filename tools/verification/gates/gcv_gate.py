# -*- coding: utf-8 -*-
"""GCV Gate - Global Coverage Validation"""

from typing import Dict, Any
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from corporate_earnings_engine.providers.router import ProviderRouter


class GCVGate:
    """Global Coverage Validation Gate"""
    
    def __init__(self):
        self.name = "GCV"
        self.description = "Global Coverage Validation"
    
    def run(self, engine_id: str) -> Dict[str, Any]:
        if engine_id != "ECO-002":
            return {
                "name": self.name,
                "description": self.description,
                "status": "NOT_APPLICABLE",
                "score": 100,
                "checks": [],
                "issues": []
            }
        
        os.environ['FINNHUB_API_KEY'] = 'd9eto3pr01qq0pmi2hs0d9eto3pr01qq0pmi2hsg'
        router = ProviderRouter()
        
        regions = {
            "US": {
                "symbols": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
                "min_required": 3,
                "currency": "USD"
            },
            "Eurozone": {
                "symbols": ["SAP", "ASML"],
                "min_required": 1,
                "currency": "EUR"
            },
            "UK": {
                "symbols": ["BP.L", "SHEL.L", "HSBA.L"],
                "min_required": 1,
                "currency": "GBP"
            },
            "Japan": {
                "symbols": ["9984.T", "6758.T"],
                "min_required": 1,
                "currency": "JPY"
            },
            "Switzerland": {
                "symbols": ["NESN.SW", "ROG.SW"],
                "min_required": 1,
                "currency": "CHF"
            },
            "Canada": {
                "symbols": ["RY.TO", "TD.TO"],
                "min_required": 1,
                "currency": "CAD"
            },
            "Australia": {
                "symbols": ["BHP.AX", "CBA.AX"],
                "min_required": 1,
                "currency": "AUD"
            },
            "New Zealand": {
                "symbols": ["AIA.NZ", "FPH.NZ"],
                "min_required": 1,
                "currency": "NZD"
            }
        }
        
        result = {
            "name": self.name,
            "description": self.description,
            "status": "PENDING",
            "score": 0,
            "checks": [],
            "issues": [],
            "details": {}
        }
        
        passed = 0
        total = len(regions)
        coverage_details = {}
        
        for region_name, region_config in regions.items():
            check = {
                "name": region_name,
                "status": "PENDING",
                "message": "",
                "symbols_found": [],
                "symbols_with_data": [],
                "currency": region_config.get("currency", "USD"),
                "provider_used": None
            }
            
            try:
                results = router.get_earnings_for_symbols(region_config["symbols"])
                
                for symbol, data in results.items():
                    if data:
                        check["symbols_with_data"].append(symbol)
                        if not check["provider_used"]:
                            check["provider_used"] = data[0].source
                
                check["symbols_found"] = check["symbols_with_data"]
                check["total_symbols"] = len(region_config["symbols"])
                
                if len(check["symbols_with_data"]) >= region_config["min_required"]:
                    check["status"] = "PASS"
                    check["message"] = f"{len(check['symbols_with_data'])}/{len(region_config['symbols'])} symbols"
                    passed += 1
                elif len(check["symbols_with_data"]) > 0:
                    check["status"] = "PARTIAL"
                    check["message"] = f"{len(check['symbols_with_data'])}/{len(region_config['symbols'])} symbols"
                else:
                    check["status"] = "FAIL"
                    check["message"] = "No data available"
                    result["issues"].append({"region": region_name, "message": "No earnings data available"})
                
                coverage_details[region_name] = {
                    "covered": len(check["symbols_with_data"]),
                    "total": len(region_config["symbols"]),
                    "provider": check.get("provider_used"),
                    "status": check["status"]
                }
                
            except Exception as e:
                check["status"] = "ERROR"
                check["message"] = str(e)
                result["issues"].append({"region": region_name, "message": str(e)})
            
            result["checks"].append(check)
        
        result["score"] = int((passed / total) * 100) if total > 0 else 0
        result["details"]["total_regions"] = total
        result["details"]["passed_regions"] = passed
        result["details"]["coverage_percentage"] = result["score"]
        result["details"]["coverage_details"] = coverage_details
        
        if result["score"] >= 80:
            result["status"] = "PASS"
        elif result["score"] >= 50:
            result["status"] = "PARTIAL"
        else:
            result["status"] = "FAIL"
        
        return result
