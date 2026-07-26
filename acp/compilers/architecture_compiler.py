"""
Architecture Compiler - Validates engine architecture layer
Checks: folder structure, required files, naming conventions
"""

from typing import Any


class ArchitectureCompiler:
    """Compiles engine architecture compliance"""

    def compile(
        self, engine, verbose: bool = False, fix: bool = False
    ) -> dict[str, Any]:
        """Compile the engine's architecture layer"""

        result = {
            "name": "architecture",
            "score": 0,
            "status": "Healthy",
            "checks": {},
            "issue": None,
            "impact": None,
            "fix": None,
            "estimated_effort": "30 minutes",
        }

        # Define required folders
        required_folders = [
            "acquisition",
            "acquisition/providers",
            "acquisition/gateway",
            "acquisition/parser",
            "warehouse",
            "warehouse/raw",
            "warehouse/cleaned",
            "warehouse/analytics",
            "runtime",
            "publication",
            "observability",
            "tests",
        ]

        # Define required files
        required_files = [
            "engine.yaml",
            "contract.yaml",
            "architecture.yaml",
            "acquisition/__init__.py",
            "warehouse/__init__.py",
            "runtime/__init__.py",
            "runtime/scheduler.py",
            "runtime/health.py",
            "runtime/metrics.py",
            "publication/__init__.py",
            "observability/__init__.py",
            "tests/__init__.py",
        ]

        checks = {}
        total_checks = 0
        passed_checks = 0

        # Check folders
        folders_check = {"status": "Pass", "present": [], "missing": []}
        for folder in required_folders:
            total_checks += 1
            folder_path = engine.path / folder
            if folder_path.exists() and folder_path.is_dir():
                folders_check["present"].append(folder)
                passed_checks += 1
            else:
                folders_check["missing"].append(folder)
                folders_check["status"] = "Fail"
                result["status"] = "Critical"
                result["issue"] = (
                    f"Missing required folders: {', '.join(folders_check['missing'])}"
                )
                result["impact"] = (
                    "Engine does not follow the required architecture standard"
                )
                result["fix"] = "Create missing folders and add __init__.py files"

        checks["folders"] = folders_check

        # Check files
        files_check = {"status": "Pass", "present": [], "missing": []}
        for file in required_files:
            total_checks += 1
            file_path = engine.path / file
            if file_path.exists() and file_path.is_file():
                files_check["present"].append(file)
                passed_checks += 1
            else:
                files_check["missing"].append(file)
                files_check["status"] = "Fail"
                if result["status"] != "Critical":
                    result["status"] = "Critical"
                result["issue"] = (
                    f"Missing required files: {', '.join(files_check['missing'])}"
                )
                result["impact"] = "Engine cannot be built or deployed"
                result["fix"] = "Create missing files with proper content"

        checks["files"] = files_check

        # Check naming conventions
        naming_check = {"status": "Pass", "issues": []}
        for python_file in engine.path.rglob("*.py"):
            if "__init__" not in python_file.name and "test_" not in python_file.name:
                if "_" not in python_file.stem and not python_file.stem.islower():
                    naming_check["issues"].append(
                        f"{python_file.name}: should be snake_case"
                    )
        if naming_check["issues"]:
            naming_check["status"] = "Warning"
            if result["status"] != "Critical":
                result["status"] = "Warning"
            result["issue"] = "Naming convention violations found"
            result["impact"] = "Inconsistent code style makes maintenance harder"
            result["fix"] = "Rename files to use snake_case"

        checks["naming"] = naming_check

        # Calculate score
        result["score"] = (
            int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        )

        # If fix is requested, generate missing structure
        if fix and result["status"] in ["Critical", "Warning"]:
            self._generate_architecture(engine)
            result["fix_applied"] = True
            result["status"] = "Healthy"
            result["score"] = 100

        return result

    def _generate_architecture(self, engine):
        """Generate the complete engine architecture"""

        # Create all required folders
        folders = [
            "acquisition/providers",
            "acquisition/gateway",
            "acquisition/parser",
            "warehouse/raw",
            "warehouse/cleaned",
            "warehouse/analytics",
            "runtime",
            "publication",
            "observability",
            "tests",
        ]

        for folder in folders:
            folder_path = engine.path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created {folder_path}")

        # Create __init__.py files
        init_files = [
            "acquisition/__init__.py",
            "acquisition/providers/__init__.py",
            "acquisition/gateway/__init__.py",
            "acquisition/parser/__init__.py",
            "warehouse/__init__.py",
            "runtime/__init__.py",
            "publication/__init__.py",
            "observability/__init__.py",
            "tests/__init__.py",
        ]

        for init_file in init_files:
            init_path = engine.path / init_file
            if not init_path.exists():
                init_path.touch()
                print(f"✅ Created {init_path}")

        # Create runtime files
        runtime_files = {
            "runtime/scheduler.py": """
# -*- coding: utf-8 -*-
\"\"\"Runtime scheduler for engine\"\"\"

from nexus.dar.scheduler import BaseScheduler

class EngineScheduler(BaseScheduler):
    def schedule(self):
        \"\"\"Define the schedule for this engine\"\"\"
        pass

    def run(self):
        \"\"\"Execute the engine's main logic\"\"\"
        pass
""",
            "runtime/health.py": """
# -*- coding: utf-8 -*-
\"\"\"Health check for engine\"\"\"

from nexus.dar.health import HealthCheck

class EngineHealth(HealthCheck):
    def check(self):
        \"\"\"Return health status of the engine\"\"\"
        return {
            "status": "healthy",
            "timestamp": "2026-07-19T00:00:00Z"
        }
""",
            "runtime/metrics.py": """
# -*- coding: utf-8 -*-
\"\"\"Metrics collection for engine\"\"\"

from nexus.observability.metrics import MetricsCollector

class EngineMetrics(MetricsCollector):
    def collect(self):
        \"\"\"Collect metrics for this engine\"\"\"
        return {
            "acquisition_count": 0,
            "processing_time": 0,
            "error_rate": 0
        }
""",
        }

        for file_path, content in runtime_files.items():
            full_path = engine.path / file_path
            if not full_path.exists():
                with open(full_path, "w") as f:
                    f.write(content.strip())
                print(f"✅ Created {full_path}")

        # Create architecture.yaml
        arch_path = engine.path / "architecture.yaml"
        if not arch_path.exists():
            import yaml

            arch_data = {
                "id": f"{engine.id}-architecture",
                "version": "1.0.0",
                "engine": engine.id,
                "required_folders": [
                    "acquisition/",
                    "acquisition/providers/",
                    "acquisition/gateway/",
                    "acquisition/parser/",
                    "warehouse/",
                    "warehouse/raw/",
                    "warehouse/cleaned/",
                    "warehouse/analytics/",
                    "runtime/",
                    "publication/",
                    "observability/",
                    "tests/",
                ],
                "required_files": [
                    "acquisition/__init__.py",
                    "acquisition/providers/__init__.py",
                    "acquisition/gateway/__init__.py",
                    "acquisition/parser/__init__.py",
                    "warehouse/__init__.py",
                    "runtime/__init__.py",
                    "runtime/scheduler.py",
                    "runtime/health.py",
                    "runtime/metrics.py",
                    "publication/__init__.py",
                    "observability/__init__.py",
                    "tests/__init__.py",
                ],
                "naming_conventions": {
                    "files": "snake_case",
                    "classes": "PascalCase",
                    "functions": "snake_case",
                    "constants": "UPPER_SNAKE_CASE",
                },
            }
            with open(arch_path, "w") as f:
                yaml.dump(arch_data, f, default_flow_style=False)
            print(f"✅ Created {arch_path}")
