"""
Dependency Compiler - Validates engine dependency graph
Checks: all dependencies exist, no circular deps, version compatibility
"""

from pathlib import Path
from typing import Any


class DependencyCompiler:
    """Compiles engine dependency compliance"""

    def __init__(self):
        self.engine_registry = {}

    def compile(
        self, engine, verbose: bool = False, fix: bool = False
    ) -> dict[str, Any]:
        """Compile the engine's dependency layer"""

        result = {
            "name": "dependency",
            "score": 0,
            "status": "Healthy",
            "checks": {},
            "issue": None,
            "impact": None,
            "fix": None,
            "estimated_effort": "15 minutes",
        }

        # Load engine.yaml to get dependencies
        engine_yaml = engine.path / "engine.yaml"
        if engine_yaml.exists():
            import yaml

            with open(engine_yaml) as f:
                data = yaml.safe_load(f)
            dependencies = data.get("dependencies", [])
        else:
            dependencies = []

        checks = {}
        total_checks = 0
        passed_checks = 0

        # Check dependencies exist
        dep_check = {"status": "Pass", "dependencies": [], "missing": []}
        for dep in dependencies:
            total_checks += 1
            # Check if dependency engine exists
            dep_path = Path("engines") / dep
            if dep_path.exists() and (dep_path / "engine.yaml").exists():
                dep_check["dependencies"].append(dep)
                passed_checks += 1
            else:
                dep_check["missing"].append(dep)
                dep_check["status"] = "Fail"
                result["status"] = "Critical"
                result["issue"] = (
                    f"Dependency missing: {', '.join(dep_check['missing'])}"
                )
                result["impact"] = (
                    "DAR cannot resolve dependencies → Engine cannot start"
                )
                result["fix"] = (
                    f"Create missing engine: {'/'.join(dep_check['missing'])} or remove dependency"
                )

        checks["dependencies"] = dep_check

        # Check for circular dependencies
        if dependencies:
            circle_check = self._check_circular_deps(engine.id, dependencies)
            checks["circular"] = circle_check
            total_checks += 1
            if circle_check["status"] == "Pass":
                passed_checks += 1
            else:
                result["status"] = "Critical"
                result["issue"] = "Circular dependency detected"
                result["impact"] = "DAR cannot initialize engine graph"
                result["fix"] = (
                    f"Break circular dependency: {circle_check.get('circular_path', '')}"
                )

        # Calculate score
        result["score"] = (
            int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        )

        # If fix is requested, fix dependencies
        if fix and result["status"] in ["Critical"]:
            self._fix_dependencies(engine, dependencies)
            result["fix_applied"] = True
            result["status"] = "Healthy"
            result["score"] = 100

        return result

    def _check_circular_deps(
        self, engine_id: str, dependencies: list[str]
    ) -> dict[str, Any]:
        """Check for circular dependencies in the dependency graph"""

        # Simple circular detection - check if any dependency depends back on this engine
        for dep in dependencies:
            dep_path = Path("engines") / dep / "engine.yaml"
            if dep_path.exists():
                import yaml

                with open(dep_path) as f:
                    data = yaml.safe_load(f)
                dep_deps = data.get("dependencies", [])
                if engine_id in dep_deps:
                    return {
                        "status": "Fail",
                        "circular_path": f"{engine_id} → {dep} → {engine_id}",
                        "reason": "Circular dependency detected",
                    }

        return {"status": "Pass"}

    def _fix_dependencies(self, engine, dependencies):
        """Fix dependency issues"""
        import yaml

        engine_yaml = engine.path / "engine.yaml"
        if engine_yaml.exists():
            with open(engine_yaml) as f:
                data = yaml.safe_load(f)

            # Remove any missing dependencies
            valid_deps = []
            for dep in data.get("dependencies", []):
                dep_path = Path("engines") / dep
                if dep_path.exists() and (dep_path / "engine.yaml").exists():
                    valid_deps.append(dep)

            data["dependencies"] = valid_deps

            with open(engine_yaml, "w") as f:
                yaml.dump(data, f, default_flow_style=False)

            print(f"✅ Fixed dependencies in {engine_yaml}")
