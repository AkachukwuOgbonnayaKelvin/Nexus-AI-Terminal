"""
EIV Gate - Engine Integration Validation
Verifies that the engine can integrate with the platform
"""

import sys
from pathlib import Path
from typing import Any

import yaml

# Add parent to path for resolver
sys.path.insert(0, str(Path(__file__).parent.parent))
from resolver import get_resolver


class EIVGate:
    """Engine Integration Validation Gate"""

    def __init__(self):
        self.name = "EIV"
        self.description = "Engine Integration Validation"
        self.resolver = get_resolver()

    def run(self, engine_id: str) -> dict[str, Any]:
        result = {
            "name": self.name,
            "description": self.description,
            "status": "PENDING",
            "score": 0,
            "checks": [],
            "issues": [],
            "diagnostics": {},
        }

        # Resolve engine identity
        identity = self.resolver.resolve(engine_id)
        if not identity:
            result["status"] = "FAIL"
            result["score"] = 0
            result["issues"].append(
                {
                    "check": "discovery",
                    "status": "FAIL",
                    "message": f"Engine '{engine_id}' not found",
                    "fix": "Check engine ID or register engine",
                }
            )
            return result

        engine_path = identity.path

        # Run integration checks with detailed diagnostics
        checks = [
            ("engine_discovery", self._check_engine_discovery, engine_path),
            ("engine_config", self._check_engine_config, engine_path),
            ("provider_connection", self._check_provider_connection, engine_path),
            ("warehouse_connection", self._check_warehouse_connection, engine_path),
            ("ndip_connection", self._check_ndip_connection, engine_path),
            ("dar_registration", self._check_dar_registration, engine_path),
        ]

        passed = 0
        total_weighted = 0

        for check_name, check_func, check_path in checks:
            check_result = check_func(check_path)
            check_result["name"] = check_name
            result["checks"].append(check_result)

            # Store diagnostics
            if "diagnostics" in check_result:
                result["diagnostics"][check_name] = check_result["diagnostics"]

            if check_result["status"] == "PASS":
                passed += 10
            elif check_result["status"] == "WARN":
                passed += 5
            total_weighted += 10

        result["score"] = (
            int((passed / total_weighted) * 100) if total_weighted > 0 else 0
        )

        failures = [c for c in result["checks"] if c["status"] == "FAIL"]
        if failures:
            result["status"] = "FAIL"
            for f in failures:
                result["issues"].append(f)
        elif result["score"] >= 80:
            result["status"] = "PASS"
        else:
            result["status"] = "PARTIAL"

        return result

    def _check_engine_discovery(self, engine_path: Path) -> dict[str, Any]:
        engine_yaml = engine_path / "engine.yaml"
        if engine_yaml.exists():
            return {"status": "PASS", "message": f"Engine found at {engine_path}"}
        return {"status": "FAIL", "message": "engine.yaml not found"}

    def _check_engine_config(self, engine_path: Path) -> dict[str, Any]:
        """Check if engine has valid configuration with detailed diagnostics"""
        result = {
            "status": "PASS",
            "message": "Configuration is valid",
            "diagnostics": {
                "missing_fields": [],
                "invalid_fields": [],
                "found_fields": [],
            },
        }

        engine_yaml = engine_path / "engine.yaml"
        if not engine_yaml.exists():
            result["status"] = "FAIL"
            result["message"] = "engine.yaml not found"
            return result

        try:
            with open(engine_yaml) as f:
                data = yaml.safe_load(f)

            # Handle nested format
            if "engine" in data and isinstance(data["engine"], dict):
                data = data["engine"]

            # Check required fields
            required_fields = ["id", "name", "version"]
            for field in required_fields:
                if data.get(field):
                    result["diagnostics"]["found_fields"].append(field)
                else:
                    result["diagnostics"]["missing_fields"].append(field)

            # Check optional but recommended fields
            optional_fields = ["domain", "stage", "description"]
            for field in optional_fields:
                if field in data:
                    result["diagnostics"]["found_fields"].append(field)

            # Check integration section
            if "integration" in data:
                integration = data["integration"]
                if isinstance(integration, dict):
                    for key in integration:
                        result["diagnostics"]["found_fields"].append(
                            f"integration.{key}"
                        )

            # Determine status
            if result["diagnostics"]["missing_fields"]:
                result["status"] = "FAIL"
                result["message"] = (
                    f"Missing required fields: {', '.join(result['diagnostics']['missing_fields'])}"
                )
                result["fix"] = (
                    f"Add missing fields to engine.yaml: {', '.join(result['diagnostics']['missing_fields'])}"
                )

        except Exception as e:
            result["status"] = "FAIL"
            result["message"] = f"YAML parsing error: {e}"

        return result

    def _check_provider_connection(self, engine_path: Path) -> dict[str, Any]:
        provider_paths = [
            engine_path / "providers",
            engine_path / "acquisition" / "providers",
            engine_path / "collectors",
            engine_path / "acquisition",
        ]
        for path in provider_paths:
            if path.exists() and any(path.glob("*.py")):
                return {
                    "status": "PASS",
                    "message": f"Provider modules found in {path.name}",
                }
        return {"status": "WARN", "message": "No provider modules found (optional)"}

    def _check_warehouse_connection(self, engine_path: Path) -> dict[str, Any]:
        warehouse_path = engine_path / "warehouse"
        if warehouse_path.exists() and any(warehouse_path.glob("*.py")):
            return {"status": "PASS", "message": "Warehouse modules found"}
        return {"status": "WARN", "message": "No warehouse modules found (optional)"}

    def _check_ndip_connection(self, engine_path: Path) -> dict[str, Any]:
        publication_path = engine_path / "publication"
        if publication_path.exists() and any(publication_path.glob("*.py")):
            return {"status": "PASS", "message": "NDIP publication modules found"}
        return {
            "status": "WARN",
            "message": "No NDIP publication modules found (optional)",
        }

    def _check_dar_registration(self, engine_path: Path) -> dict[str, Any]:
        engine_yaml = engine_path / "engine.yaml"
        if engine_yaml.exists():
            try:
                with open(engine_yaml) as f:
                    data = yaml.safe_load(f)

                if "engine" in data and isinstance(data["engine"], dict):
                    data = data["engine"]

                if "integration" in data and data["integration"].get("dar") is True:
                    return {"status": "PASS", "message": "DAR integration configured"}
                if data.get("runtime", {}).get("managed_by") == "DAR":
                    return {"status": "PASS", "message": "DAR integration configured"}
            except Exception:
                pass
        return {
            "status": "WARN",
            "message": "DAR integration not configured (optional)",
        }
