# -*- coding: utf-8 -*-
"""Report Generator for Raw Backend Certification"""

from typing import Dict, Any
from datetime import datetime


class ReportGenerator:
    """Generates certification reports"""
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
    
    def print_summary(self):
        """Print summary report"""
        print("\n" + "="*70)
        print("  RAW BACKEND CERTIFICATION SUMMARY")
        print("="*70)
        print("")
        
        if not self.results:
            print("  No results to display.")
            return
        
        # Engine summary table
        print("┌──────────┬─────────────────────────────────┬────────────┐")
        print("│ Engine   │ Name                            │ Status     │")
        print("├──────────┼─────────────────────────────────┼────────────┤")
        
        for engine_id, result in self.results.items():
            if result.status == "CERTIFIED":
                status_icon = "✅"
            elif result.status == "PARTIAL":
                status_icon = "⚠️"
            else:
                status_icon = "❌"
            print(f"│ {engine_id:<8} │ {result.engine_name:<31} │ {status_icon} {result.status:<9} │")
        
        print("└──────────┴─────────────────────────────────┴────────────┘")
        print("")
        
        # Detailed results
        for engine_id, result in self.results.items():
            print("")
            print("-"*70)
            print(f"  {engine_id}: {result.engine_name}")
            print(f"  Status: {result.status}")
            print("-"*70)
            
            for check in result.checks:
                if check.status == "PASS":
                    status_icon = "✅"
                elif check.status == "WARNING":
                    status_icon = "⚠️"
                else:
                    status_icon = "❌"
                print(f"  {status_icon} {check.name:<12} : {check.message}")
                
                if check.details:
                    for key, value in check.details.items():
                        if isinstance(value, list) and len(value) > 5:
                            print(f"      {key}: {len(value)} items")
                        else:
                            print(f"      {key}: {value}")
            
            print("")
        
        print("="*70)
        
        # Overall status
        statuses = [r.status for r in self.results.values()]
        if all(s == "CERTIFIED" for s in statuses):
            print("  ✅ RAW BACKEND: CERTIFIED")
            print("  ✅ All engines passed. Consumer engines can begin.")
        elif any(s == "FAILED" for s in statuses):
            print("  ❌ RAW BACKEND: NOT CERTIFIED")
            print("  ❌ Some engines failed. Fix the issues above.")
        else:
            print("  ⚠️ RAW BACKEND: PARTIAL")
            print("  ⚠️ Some warnings found. Review the report above.")
        
        print("="*70)
        print("")
