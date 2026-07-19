# -*- coding: utf-8 -*-
"""Visualizer - Renders ACP output in human-readable format"""

from typing import Dict, Any
import json
from datetime import datetime


class Visualizer:
    """Visualizes compilation results"""
    
    def __init__(self, result: Dict[str, Any]):
        self.result = result
    
    def render(self, output_format: str = "text"):
        """Render the output in the specified format"""
        self._render_text()
    
    def _render_text(self):
        """Render text-based output"""
        
        print("")
        print("="*70)
        print("  ACP ARCHITECTURE OS v2.0.0")
        print("  Platform: Nexus AI Terminal")
        print("  Timestamp: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*70)
        
        if "error" in self.result:
            print(f"\n[ERROR] {self.result['error']}")
            return
        
        # Render each engine
        engines = self.result.get("engines", [])
        if not engines:
            print("\n[INFO] No engines found to validate")
            return
        
        print(f"\n[STATUS] Validating {len(engines)} engine(s)...")
        print("-"*70)
        
        for engine in engines:
            # Determine status indicator
            if engine["status"] == "Healthy":
                status_indicator = "[OK]"
            elif engine["status"] == "Warning":
                status_indicator = "[WARN]"
            else:
                status_indicator = "[FAIL]"
            
            print(f"\n{status_indicator} {engine['id']}: {engine['name']}")
            print(f"   Status: {engine['status']}")
            print(f"   Score: {engine.get('overall_score', 0)}%")
            
            # Show layer details
            for layer, layer_result in engine.get("layers", {}).items():
                layer_status = layer_result.get("status", "Unknown")
                layer_score = layer_result.get("score", 0)
                
                if layer_status == "Healthy":
                    layer_indicator = "[OK]"
                elif layer_status == "Warning":
                    layer_indicator = "[WARN]"
                else:
                    layer_indicator = "[FAIL]"
                
                print(f"   {layer_indicator} {layer}: {layer_score}%")
                
                # Show issues if any
                if layer_result.get("issue"):
                    print(f"      Issue: {layer_result['issue']}")
                if layer_result.get("impact"):
                    print(f"      Impact: {layer_result['impact']}")
                if layer_result.get("fix"):
                    print(f"      Fix: {layer_result['fix']}")
        
        # Render platform score
        platform_score = self.result.get("platform_score", {})
        if platform_score:
            print("\n" + "-"*70)
            print("  PLATFORM SCORE")
            print("-"*70)
            
            for layer, score in platform_score.items():
                bar_length = int(score / 2)
                bar = "#" * bar_length + "." * (50 - bar_length)
                print(f"  {layer.capitalize():12} {score:3}%  {bar}")
        
        # Render repair plan
        repair_plan = self.result.get("repair_plan", [])
        if repair_plan:
            print("\n" + "-"*70)
            print("  REPAIR PLAN")
            print("-"*70)
            
            for item in repair_plan:
                priority_icon = "[CRITICAL]" if item["priority"] == "Critical" else "[WARN]"
                print(f"  {priority_icon} {item['engine']} - {item['layer']}")
                print(f"     Issue: {item['issue']}")
                print(f"     Fix: {item['fix']}")
                if item.get("estimated_effort"):
                    print(f"     Effort: {item['estimated_effort']}")
        
        # Render build decision
        build = self.result.get("build_decision", {})
        print("\n" + "-"*70)
        print("  BUILD DECISION")
        print("-"*70)
        
        if build.get("blocked"):
            print("  [BLOCKED] Build cannot proceed")
            print(f"  Reason: {build.get('reason', 'Unknown')}")
        else:
            print("  [ALLOWED] Build can proceed")
            print(f"  Reason: {build.get('reason', 'All checks passed')}")
        
        print("="*70 + "\n")
    
    def _render_json(self):
        """Render JSON output"""
        print(json.dumps(self.result, indent=2, default=str))
