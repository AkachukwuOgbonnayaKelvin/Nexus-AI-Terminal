# -*- coding: utf-8 -*-
"""
ACP Gate - Architecture Compliance Validation
Verifies that the engine is structurally correct
"""

import subprocess
import json
import sys
import re
from pathlib import Path
from typing import Dict, Any

# Add parent to path for resolver
sys.path.insert(0, str(Path(__file__).parent.parent))
from resolver import get_resolver


class ACPGate:
    """Architecture compliance gate"""
    
    def __init__(self):
        self.name = "ACP"
        self.description = "Architecture Compliance Validation"
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.resolver = get_resolver()
    
    def run(self, engine_id: str) -> Dict[str, Any]:
        """Run ACP validation on the engine"""
        result = {
            "name": self.name,
            "description": self.description,
            "status": "PENDING",
            "score": 0,
            "details": {},
            "checks": [],
            "issues": []
        }
        
        # Resolve engine identity first
        identity = self.resolver.resolve(engine_id)
        if not identity:
            result["status"] = "FAIL"
            result["score"] = 0
            result["issues"].append({
                "check": "discovery",
                "status": "FAIL",
                "message": f"Engine '{engine_id}' not found",
                "fix": "Check engine ID and ensure engine.yaml exists"
            })
            return result
        
        # Use the resolved engine ID for ACP
        resolved_id = identity.id
        
        try:
            # Run ACP on the resolved engine ID
            cmd = ["python", str(self.project_root / "acp" / "acp.py"), "engine", resolved_id]
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.project_root))
            
            output = proc.stdout
            
            # Parse the text output
            compliance_match = re.search(r"Architecture Compliance:\s*(\d+)%", output)
            maturity_match = re.search(r"Architecture Maturity:\s*(\d+)%", output)
            overall_match = re.search(r"Overall Health:\s*(\d+)%", output)
            status_match = re.search(r"Status:\s*(\w+)", output)
            
            if overall_match:
                result["score"] = int(overall_match.group(1))
                
                if compliance_match:
                    result["details"]["compliance"] = int(compliance_match.group(1))
                if maturity_match:
                    result["details"]["maturity"] = int(maturity_match.group(1))
                if status_match:
                    result["details"]["status"] = status_match.group(1)
                
                # Check for issues in output
                if "ERROR" in output or "CRITICAL" in output:
                    result["status"] = "FAIL"
                    error_lines = [line for line in output.split('\n') if 'ERROR' in line or 'CRITICAL' in line]
                    for line in error_lines[:5]:
                        result["issues"].append({
                            "check": "architecture",
                            "status": "FAIL",
                            "message": line.strip()
                        })
                elif "WARNING" in output:
                    result["status"] = "PARTIAL"
                    warning_lines = [line for line in output.split('\n') if 'WARNING' in line]
                    for line in warning_lines[:5]:
                        result["issues"].append({
                            "check": "architecture",
                            "status": "WARN",
                            "message": line.strip()
                        })
                elif result["score"] >= 90:
                    result["status"] = "PASS"
                elif result["score"] >= 70:
                    result["status"] = "PARTIAL"
                else:
                    result["status"] = "FAIL"
                
                # Add success checks
                if result["status"] != "FAIL":
                    result["checks"].append({
                        "name": "architecture_compliance",
                        "status": "PASS",
                        "message": f"Compliance: {result['details'].get('compliance', 0)}%"
                    })
                    result["checks"].append({
                        "name": "architecture_maturity",
                        "status": "PASS",
                        "message": f"Maturity: {result['details'].get('maturity', 0)}%"
                    })
            
            elif "No engine found" in output or "not found" in output:
                result["status"] = "FAIL"
                result["issues"].append({
                    "check": "discovery",
                    "status": "FAIL",
                    "message": f"Engine '{resolved_id}' not found by ACP",
                    "fix": "Ensure engine is registered in ACP's engine registry"
                })
            
            else:
                result["status"] = "FAIL"
                result["issues"].append({
                    "check": "execution",
                    "status": "FAIL",
                    "message": "ACP execution produced no valid output",
                    "fix": "Check ACP configuration and run manually"
                })
        
        except Exception as e:
            result["status"] = "FAIL"
            result["issues"].append({
                "check": "runtime",
                "status": "FAIL",
                "message": str(e),
                "fix": "Check Python installation and dependencies"
            })
        
        # Ensure score is set
        if result["score"] == 0 and result["status"] == "PASS":
            result["score"] = 100
        
        return result
