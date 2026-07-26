"""
Platform Compiler - Validates overall platform health
Checks: all engines healthy, no critical failures, production readiness
"""

from typing import Any


class PlatformCompiler:
    """Compiles overall platform health"""

    def compile(
        self, engine, verbose: bool = False, fix: bool = False
    ) -> dict[str, Any]:
        """Compile the platform layer for an engine"""

        result = {
            "name": "platform",
            "score": 0,
            "status": "Healthy",
            "checks": {},
            "issue": None,
            "impact": None,
            "fix": None,
            "estimated_effort": "1 hour",
        }

        checks = {}
        total_checks = 0
        passed_checks = 0

        # Check tests exist
        total_checks += 1
        test_path = engine.path / "tests"
        if test_path.exists():
            test_files = list(test_path.glob("test_*.py"))
            if test_files:
                checks["tests"] = {"status": "Pass", "count": len(test_files)}
                passed_checks += 1
            else:
                checks["tests"] = {"status": "Fail", "reason": "No test files found"}
                result["status"] = "Warning"
                result["issue"] = "No tests found"
                result["impact"] = "Cannot verify engine correctness"
                result["fix"] = "Add tests in tests/ directory"
        else:
            checks["tests"] = {"status": "Fail", "reason": "tests/ directory missing"}
            result["status"] = "Warning"
            result["issue"] = "tests/ directory missing"
            result["impact"] = "Cannot verify engine correctness"
            result["fix"] = "Create tests/ directory with test files"

        # Check documentation
        total_checks += 1
        docs_checks = []
        for doc_file in ["README.md", "docs/README.md"]:
            doc_path = engine.path / doc_file
            if doc_path.exists():
                docs_checks.append(True)
        if docs_checks:
            checks["documentation"] = {"status": "Pass", "files": docs_checks}
            passed_checks += 1
        else:
            checks["documentation"] = {
                "status": "Fail",
                "reason": "No documentation found",
            }
            if result["status"] != "Warning":
                result["status"] = "Warning"
            result["issue"] = "No documentation found"
            result["impact"] = "New developers cannot understand this engine"
            result["fix"] = "Create README.md with engine overview"

        # Check stage and allowed failures
        total_checks += 1
        stage = engine.stage
        allowed_failures = engine.allowed_failures

        if stage in ["Development", "Testing", "Staging", "Production"]:
            checks["stage"] = {
                "status": "Pass",
                "stage": stage,
                "allowed_failures": allowed_failures,
            }
            passed_checks += 1

            # Stage-specific rules
            if stage == "Production" and allowed_failures > 0:
                checks["stage"]["warning"] = (
                    "Production engines should have 0 allowed failures"
                )
                result["status"] = "Warning"
        else:
            checks["stage"] = {
                "status": "Fail",
                "reason": f"Invalid stage: {stage}",
                "valid_stages": ["Development", "Testing", "Staging", "Production"],
            }
            result["status"] = "Warning"
            result["issue"] = f"Invalid stage: {stage}"
            result["impact"] = "Platform cannot manage deployment lifecycle"
            result["fix"] = (
                "Set stage to one of: Development, Testing, Staging, Production"
            )

        # Calculate score
        result["score"] = (
            int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        )

        return result
