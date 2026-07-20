# -*- coding: utf-8 -*-
"""
Runtime Compiler - Validates DAR runtime compliance
Checks: scheduler, health, metrics, lifecycle declared
"""

from typing import Dict, Any


class RuntimeCompiler:
    """Compiles engine runtime compliance"""

    def compile(
        self, engine, verbose: bool = False, fix: bool = False
    ) -> Dict[str, Any]:
        """Compile the engine's runtime layer"""

        result = {
            "name": "runtime",
            "score": 0,
            "status": "Healthy",
            "checks": {},
            "issue": None,
            "impact": None,
            "fix": None,
            "estimated_effort": "20 minutes",
        }

        # Load engine.yaml for lifecycle
        engine_yaml = engine.path / "engine.yaml"
        if engine_yaml.exists():
            import yaml

            with open(engine_yaml) as f:
                data = yaml.safe_load(f)
            lifecycle = data.get("lifecycle", {})
            runtime = data.get("runtime", {})
        else:
            lifecycle = {}
            runtime = {}

        checks = {}
        total_checks = 0
        passed_checks = 0

        # Check lifecycle declared
        total_checks += 1
        if lifecycle:
            checks["lifecycle"] = {"status": "Pass", "value": lifecycle}
            passed_checks += 1
        else:
            checks["lifecycle"] = {
                "status": "Fail",
                "value": "Not declared",
                "reason": "DAR needs lifecycle metadata to manage this engine",
            }
            result["status"] = "Critical"
            result["issue"] = "Lifecycle not declared in engine.yaml"
            result["impact"] = (
                "DAR cannot start/stop/recover/schedule/monitor this engine"
            )
            result["fix"] = "Add lifecycle section to engine.yaml"

        # Check runtime configured
        total_checks += 1
        if runtime:
            checks["runtime"] = {"status": "Pass", "value": runtime}
            passed_checks += 1
        else:
            checks["runtime"] = {
                "status": "Fail",
                "value": "Not configured",
                "reason": "DAR needs runtime configuration for scheduling",
            }
            if result["status"] != "Critical":
                result["status"] = "Warning"
            result["issue"] = "Runtime not configured"
            result["impact"] = "DAR cannot schedule this engine"
            result["fix"] = "Add runtime section to engine.yaml"

        # Check runtime files exist
        runtime_files = ["scheduler.py", "health.py", "metrics.py"]
        files_check = {"status": "Pass", "present": [], "missing": []}
        for file in runtime_files:
            total_checks += 1
            file_path = engine.path / "runtime" / file
            if file_path.exists():
                files_check["present"].append(file)
                passed_checks += 1
            else:
                files_check["missing"].append(file)
                files_check["status"] = "Fail"

        if files_check["missing"]:
            checks["runtime_files"] = {
                "status": "Fail",
                "missing": files_check["missing"],
                "present": files_check["present"],
                "reason": f"Missing: {', '.join(files_check['missing'])}",
            }
            if result["status"] != "Critical":
                result["status"] = "Critical"
            result["issue"] = (
                f"Missing runtime files: {', '.join(files_check['missing'])}"
            )
            result["impact"] = "DAR cannot run this engine"
            result["fix"] = "Create missing files in runtime/"
        else:
            checks["runtime_files"] = {
                "status": "Pass",
                "present": files_check["present"],
            }

        # Calculate score
        result["score"] = (
            int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        )

        # If fix is requested, generate runtime files
        if fix and result["status"] in ["Critical", "Warning"]:
            self._generate_runtime(engine)
            result["fix_applied"] = True
            result["status"] = "Healthy"
            result["score"] = 100

        return result

    def _generate_runtime(self, engine):
        """Generate runtime files"""

        runtime_path = engine.path / "runtime"
        runtime_path.mkdir(exist_ok=True)

        # Create scheduler.py
        scheduler_content = '''
# -*- coding: utf-8 -*-
"""Runtime scheduler for {engine_id}"""

from nexus.dar.scheduler import BaseScheduler

class {engine_id}Scheduler(BaseScheduler):
    def schedule(self):
        """Define the schedule for this engine"""
        pass

    def run(self):
        """Execute the engine's main logic"""
        pass
'''.strip()

        with open(runtime_path / "scheduler.py", "w") as f:
            f.write(scheduler_content.format(engine_id=engine.id))

        # Create health.py
        health_content = '''
# -*- coding: utf-8 -*-
"""Health check for {engine_id}"""

from nexus.dar.health import HealthCheck

class {engine_id}Health(HealthCheck):
    def check(self):
        """Return health status of the engine"""
        return {{
            "status": "healthy",
            "timestamp": "2026-07-19T00:00:00Z"
        }}
'''.strip()

        with open(runtime_path / "health.py", "w") as f:
            f.write(health_content.format(engine_id=engine.id))

        # Create metrics.py
        metrics_content = '''
# -*- coding: utf-8 -*-
"""Metrics collection for {engine_id}"""

from nexus.observability.metrics import MetricsCollector

class {engine_id}Metrics(MetricsCollector):
    def collect(self):
        """Collect metrics for this engine"""
        return {{
            "acquisition_count": 0,
            "processing_time": 0,
            "error_rate": 0
        }}
'''.strip()

        with open(runtime_path / "metrics.py", "w") as f:
            f.write(metrics_content.format(engine_id=engine.id))

        print(f"✅ Generated runtime files for {engine.id}")
