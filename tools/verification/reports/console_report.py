# -*- coding: utf-8 -*-
"""
Console Report - Renders verification results in console
"""

from typing import Dict, Any


class ConsoleReport:
    """Renders verification results as console output"""
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
    
    def render(self):
        """Render the report"""
        if isinstance(self.results, dict) and "engine" in self.results:
            # Single engine report
            self._render_single(self.results)
        else:
            # Multi-engine report
            self._render_multi(self.results)
    
    def _render_single(self, result: Dict[str, Any]):
        """Render single engine report"""
        print("\n" + "="*70)
        print(f"  NEXUS ENGINE VERIFICATION REPORT")
        print(f"  Engine: {result.get('engine', 'Unknown')}")
        print("="*70)
        
        for gate_name, gate_result in result.get("gates", {}).items():
            status_icon = "✅" if gate_result.get("status") == "PASS" else "❌" if gate_result.get("status") == "FAIL" else "⚠️"
            print(f"\n[{status_icon}] {gate_name.upper()}: {gate_result.get('status', 'PENDING')}")
            print(f"   Score: {gate_result.get('score', 0)}%")
            
            for check in gate_result.get("checks", []):
                check_icon = "✅" if check.get("status") == "PASS" else "❌" if check.get("status") == "FAIL" else "⚠️"
                print(f"   {check_icon} {check.get('name', 'Unknown')}: {check.get('message', '')}")
            
            for issue in gate_result.get("issues", []):
                print(f"   ❌ {issue.get('message', 'Unknown issue')}")
                if issue.get("fix"):
                    print(f"      Fix: {issue.get('fix')}")
        
        print("\n" + "="*70)
        print(f"  OVERALL STATUS: {result.get('overall_status', 'UNKNOWN')}")
        print("="*70 + "\n")
    
    def _render_multi(self, results: Dict[str, Any]):
        """Render multi-engine report"""
        print("\n" + "="*70)
        print("  NEXUS ENGINE VERIFICATION REPORT - ALL ENGINES")
        print("="*70)
        
        for engine_id, result in results.items():
            status_icon = "✅" if result.get("overall_status") == "PASS" else "❌" if result.get("overall_status") == "FAIL" else "⚠️"
            print(f"\n[{status_icon}] {engine_id}: {result.get('overall_status', 'PENDING')}")
            
            # Calculate average score
            scores = [g.get("score", 0) for g in result.get("gates", {}).values()]
            avg_score = int(sum(scores) / len(scores)) if scores else 0
            print(f"   Average Score: {avg_score}%")
            
            # Show gate results
            for gate_name, gate_result in result.get("gates", {}).items():
                gate_icon = "✅" if gate_result.get("status") == "PASS" else "❌" if gate_result.get("status") == "FAIL" else "⚠️"
                print(f"   {gate_icon} {gate_name.upper()}: {gate_result.get('status', 'PENDING')} ({gate_result.get('score', 0)}%)")
        
        print("\n" + "="*70)
        print("  VERIFICATION COMPLETE")
        print("="*70 + "\n")
