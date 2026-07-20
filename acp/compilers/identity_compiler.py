# -*- coding: utf-8 -*-
"""
Identity Compiler - Validates engine identity layer
Checks: ID, version, owner, purpose, classification
"""

from typing import Dict, Any


class IdentityCompiler:
    """Compiles engine identity metadata"""

    def compile(
        self, engine, verbose: bool = False, fix: bool = False
    ) -> Dict[str, Any]:
        """Compile the engine's identity layer"""

        result = {
            "name": "identity",
            "score": 0,
            "status": "Healthy",
            "checks": {},
            "issue": None,
            "impact": None,
            "fix": None,
            "estimated_effort": "5 minutes",
        }

        checks = {}
        total_checks = 0
        passed_checks = 0

        # Check 1: Does engine have an ID?
        total_checks += 1
        if engine.id and engine.id.startswith(
            tuple(["GLO", "AST", "TEC", "INS", "IMT", "SEN", "MEM", "NEWS"])
        ):
            checks["id"] = {"status": "Pass", "value": engine.id}
            passed_checks += 1
        else:
            checks["id"] = {
                "status": "Fail",
                "value": engine.id or "Missing",
                "reason": "Engine ID must start with valid prefix (GLO, AST, TEC, INS, IMT, SEN, MEM, NEWS)",
            }
            result["status"] = "Critical"
            result["issue"] = "Invalid or missing engine ID"
            result["impact"] = "Engine cannot be registered with DAR"
            result["fix"] = "Set id: DOMAIN-XXX (e.g., NEWS-001)"

        # Check 2: Does engine have a version?
        total_checks += 1
        if engine.version and engine.version.count(".") == 2:
            checks["version"] = {"status": "Pass", "value": engine.version}
            passed_checks += 1
        else:
            checks["version"] = {
                "status": "Fail",
                "value": engine.version or "Missing",
                "reason": "Version must follow semantic versioning (X.Y.Z)",
            }
            if result["status"] != "Critical":
                result["status"] = "Warning"
            result["issue"] = "Invalid version format"
            result["impact"] = "Cannot track engine maturity and updates"
            result["fix"] = "Set version: 1.0.0"

        # Check 3: Does engine have an owner?
        total_checks += 1
        if engine.owner and engine.owner != "Unknown":
            checks["owner"] = {"status": "Pass", "value": engine.owner}
            passed_checks += 1
        else:
            checks["owner"] = {
                "status": "Fail",
                "value": engine.owner or "Missing",
                "reason": "Engine must have an assigned owner",
            }
            if result["status"] != "Critical":
                result["status"] = "Warning"
            result["issue"] = "No owner assigned"
            result["impact"] = "No single point of accountability"
            result["fix"] = "Set owner: Your Name or Team Name"

        # Check 4: Does engine have a purpose?
        total_checks += 1
        if engine.purpose and len(engine.purpose) > 10:
            checks["purpose"] = {
                "status": "Pass",
                "value": engine.purpose[:50] + "..."
                if len(engine.purpose) > 50
                else engine.purpose,
            }
            passed_checks += 1
        else:
            checks["purpose"] = {
                "status": "Fail",
                "value": engine.purpose or "Missing",
                "reason": "Engine must have a clear purpose statement",
            }
            if result["status"] != "Critical":
                result["status"] = "Warning"
            result["issue"] = "Missing purpose statement"
            result["impact"] = "Developers won't understand what this engine does"
            result["fix"] = "Set purpose: Clear description of what this engine does"

        # Check 5: Does engine have a classification?
        total_checks += 1
        valid_classifications = [
            "Data Acquisition",
            "Data Processing",
            "Domain Intelligence",
            "Analytics",
            "Execution",
            "Orchestration",
            "Gateway",
        ]
        if engine.classification and engine.classification in valid_classifications:
            checks["classification"] = {
                "status": "Pass",
                "value": engine.classification,
            }
            passed_checks += 1
        else:
            checks["classification"] = {
                "status": "Fail",
                "value": engine.classification or "Missing",
                "reason": f"Classification must be one of: {', '.join(valid_classifications)}",
            }
            if result["status"] != "Critical":
                result["status"] = "Warning"
            result["issue"] = "Missing or invalid classification"
            result["impact"] = "Engine placement in architecture is ambiguous"
            result["fix"] = (
                f"Set classification: One of {', '.join(valid_classifications)}"
            )

        # Calculate score
        result["score"] = (
            int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        )
        result["checks"] = checks

        # If fix is requested, generate the missing engine.yaml
        if fix and result["status"] in ["Critical", "Warning"]:
            self._generate_engine_yaml(engine)
            result["fix_applied"] = True
            result["status"] = "Healthy"
            result["score"] = 100

        return result

    def _generate_engine_yaml(self, engine):
        """Generate a complete engine.yaml file"""
        import yaml

        data = {
            "id": engine.id,
            "name": engine.name,
            "version": "1.0.0",
            "owner": "Platform Team",
            "purpose": "Engine purpose needs to be defined",
            "classification": "Domain Intelligence",
            "maturity": "Development",
            "stage": "Development",
            "allowed_failures": 10,
            "lifecycle": {
                "can_start": True,
                "can_stop": True,
                "can_recover": True,
                "can_schedule": True,
                "can_monitor": True,
                "recovery_timeout": 30,
            },
            "runtime": {
                "schedule": "*/5 * * * *",
                "priority": 3,
                "retries": 3,
                "timeout": 60,
                "retry_delay": 5,
            },
            "dependencies": [],
        }

        path = engine.path / "engine.yaml"
        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

        print(f"✅ Generated {path}")
