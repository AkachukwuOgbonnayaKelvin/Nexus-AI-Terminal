# -*- coding: utf-8 -*-
"""
Architecture Analyzer - Analyzes engine architecture compliance
"""

from pathlib import Path
from typing import Dict, Any, List


class ArchitectureAnalyzer:
    """Analyzes engine architecture - fixed scoring algorithm"""
    
    def __init__(self):
        self.required_folders = [
            "acquisition",
            "warehouse",
            "publication"
        ]
        
        self.optional_folders = [
            "runtime",
            "gateway",
            "observability",
            "tests",
            "docs"
        ]
        
        self.required_files = [
            "engine.yaml",
            "contract.yaml"
        ]
        
        self.optional_files = [
            "architecture.yaml",
            "README.md"
        ]
    
    def analyze(self, engine_path: Path, engine_data: Dict) -> Dict[str, Any]:
        """Analyze engine architecture - returns compliance and maturity separately"""
        result = {
            "compliance_score": 0,      # Required components only
            "maturity_score": 0,        # Optional components
            "overall_score": 0,         # Weighted combination
            "status": "Healthy",
            "present_folders": [],
            "missing_folders": [],
            "present_files": [],
            "missing_files": [],
            "optional_present": [],
            "optional_missing": [],
            "issues": [],
            "warnings": [],
            "info": []
        }
        
        # Check required folders
        required_present = 0
        for folder in self.required_folders:
            if (engine_path / folder).exists():
                result["present_folders"].append(folder)
                required_present += 1
            else:
                result["missing_folders"].append(folder)
                result["issues"].append({
                    "type": "MISSING_REQUIRED_FOLDER",
                    "folder": folder,
                    "severity": "Critical",
                    "message": f"Required folder '{folder}' is missing",
                    "fix": f"Create {engine_path}/{folder}/"
                })
        
        # Check required files
        required_files_present = 0
        for file in self.required_files:
            if (engine_path / file).exists():
                result["present_files"].append(file)
                required_files_present += 1
            else:
                result["missing_files"].append(file)
                result["issues"].append({
                    "type": "MISSING_REQUIRED_FILE",
                    "file": file,
                    "severity": "Critical",
                    "message": f"Required file '{file}' is missing",
                    "fix": f"Create {engine_path}/{file}"
                })
        
        # Calculate compliance score (required items only, max 100%)
        required_total = len(self.required_folders) + len(self.required_files)
        required_actual = required_present + required_files_present
        result["compliance_score"] = int((required_actual / required_total) * 100) if required_total > 0 else 100
        
        # Check optional folders (maturity)
        optional_present_count = 0
        for folder in self.optional_folders:
            if (engine_path / folder).exists():
                result["optional_present"].append(folder)
                optional_present_count += 1
            else:
                result["optional_missing"].append(folder)
                result["info"].append({
                    "type": "OPTIONAL_COMPONENT_MISSING",
                    "folder": folder,
                    "severity": "Info",
                    "message": f"Optional component '{folder}' not implemented",
                    "recommendation": f"Add only if required by engine specification"
                })
        
        # Check optional files
        optional_files_present = 0
        for file in self.optional_files:
            if (engine_path / file).exists():
                result["optional_present"].append(file)
                optional_files_present += 1
            else:
                result["optional_missing"].append(file)
                if file == "README.md":
                    result["info"].append({
                        "type": "NO_README",
                        "file": file,
                        "severity": "Info",
                        "message": "README.md not found",
                        "recommendation": "Consider adding documentation for developer onboarding"
                    })
        
        # Calculate maturity score (optional items, max 100%)
        optional_total = len(self.optional_folders) + len(self.optional_files)
        optional_actual = optional_present_count + optional_files_present
        result["maturity_score"] = int((optional_actual / optional_total) * 100) if optional_total > 0 else 0
        
        # Calculate overall score (weighted: 70% compliance, 30% maturity)
        result["overall_score"] = int((result["compliance_score"] * 0.7) + (result["maturity_score"] * 0.3))
        
        # Determine status
        if result["issues"]:
            result["status"] = "Critical"
        elif result["compliance_score"] < 80:
            result["status"] = "Warning"
        elif result["maturity_score"] < 50:
            result["status"] = "Warning"
        else:
            result["status"] = "Healthy"
        
        return result
