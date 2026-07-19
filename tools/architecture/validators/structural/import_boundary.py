"""Import Boundary Validator – Enforces layer boundaries."""

import ast
from pathlib import Path
from typing import List, Dict, Set
from tools.architecture.models import ARCResult
from tools.architecture.validators.base import BaseValidator

class ImportBoundaryValidator(BaseValidator):
    """Validates that imports respect layer boundaries."""

    # Layer definitions
    LAYERS = {
        "raw": ["*_engine", "*_warehouse", "*_collector"],
        "ndip": ["ndip"],
        "intelligence": ["*_intelligence"],
        "presentation": ["dashboard", "api", "web"],
        "foundation": ["foundation", "shared"],
    }

    # Disallowed imports
    FORBIDDEN_PATTERNS = [
        # Dashboard should not import raw engines
        ("dashboard", "*_engine", "Dashboard cannot import raw engines"),
        ("dashboard", "*_warehouse", "Dashboard cannot import warehouses"),
        # Intelligence engines should not import raw engines directly
        ("*_intelligence", "*_engine", "Intelligence cannot import raw engines directly"),
        ("*_intelligence", "*_collector", "Intelligence cannot import collectors"),
        # Raw engines should not import intelligence
        ("*_engine", "*_intelligence", "Raw engines cannot import intelligence"),
        # NDIP should not import raw engines
        ("ndip", "*_engine", "NDIP cannot import raw engines"),
    ]

    def get_severity(self) -> str:
        return "critical"

    def validate(self) -> List[ARCResult]:
        results = []
        violations = self._check_imports()
        
        if violations:
            results.append(self.result(
                False,
                f"Found {len(violations)} import boundary violations",
                details=violations[:20],
                severity="critical"
            ))
        else:
            results.append(self.result(True, "All import boundaries respected"))
        
        return results

    def _check_imports(self) -> List[Dict]:
        """Check for import boundary violations."""
        violations = []
        
        for py_file in self.root.rglob("*.py"):
            if any(e in str(py_file) for e in [".venv", "__pycache__", "tools"]):
                continue
            
            file_layer = self._get_layer(py_file)
            if not file_layer:
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if self._is_violation(alias.name, file_layer):
                                violations.append({
                                    "file": str(py_file.relative_to(self.root)),
                                    "import": alias.name,
                                    "from_layer": file_layer,
                                })
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and self._is_violation(node.module, file_layer):
                            violations.append({
                                "file": str(py_file.relative_to(self.root)),
                                "import": node.module,
                                "from_layer": file_layer,
                            })
            except Exception:
                pass
        
        return violations

    def _get_layer(self, file_path: Path) -> str:
        """Determine which layer a file belongs to."""
        path_str = str(file_path)
        if "ndip" in path_str:
            return "ndip"
        elif "dashboard" in path_str or "api" in path_str:
            return "presentation"
        elif "foundation" in path_str or "shared" in path_str:
            return "foundation"
        elif any(e in path_str for e in ["_intelligence", "_analytics"]):
            return "intelligence"
        elif any(e in path_str for e in ["_engine", "_warehouse", "_collector"]):
            return "raw"
        return "unknown"

    def _is_violation(self, import_name: str, from_layer: str) -> bool:
        """Check if an import violates boundaries."""
        # Check if the import is within the same layer
        if from_layer in ["foundation", "ndip"]:
            return False
        
        # Check forbidden patterns
        for pattern, target, message in self.FORBIDDEN_PATTERNS:
            if from_layer == pattern or pattern == "*":
                if target in import_name or target == "*":
                    return True
        
        return False
