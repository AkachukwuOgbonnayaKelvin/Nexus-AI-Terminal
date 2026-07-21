#!/usr/bin/env python3
"""
ARC-001 Architecture Compliance Engine
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class Report:
    """Architecture compliance report"""

    def __init__(self):
        self.results = {
            "status": "PENDING",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": [],
            "errors": [],
            "warnings": [],
            "summary": {},
        }

    def add_check(self, name: str, passed: bool, message: str = ""):
        self.results["checks"].append(
            {"name": name, "passed": passed, "message": message}
        )

    def add_error(self, message: str):
        self.results["errors"].append(message)

    def add_warning(self, message: str):
        self.results["warnings"].append(message)

    def finalize(self):
        self.results["status"] = "PASSED" if not self.results["errors"] else "FAILED"
        self.results["timestamp"] = datetime.utcnow().isoformat()
        return self.results


class ArchitectureEngine:
    """ARC-001 Architecture Compliance Engine"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.report: Optional[Report] = None

    def run(self) -> Dict[str, Any]:
        """Run all architecture checks"""
        self.report = Report()

        # Check directory structure
        self._check_directories()

        # Check engine structure
        self._check_engines()

        # Check hub structure
        self._check_hub()

        # Check schemas
        self._check_schemas()

        return self.report.finalize()

    def _check_directories(self):
        """Check required directories exist"""
        required = [
            "intelligence",
            "intelligence/engines",
            "intelligence/hub",
            "intelligence/schemas",
        ]

        for dir_path in required:
            full_path = self.project_root / dir_path
            if full_path.exists():
                self.report.add_check(f"Directory: {dir_path}", True, "Exists")
            else:
                self.report.add_check(
                    f"Directory: {dir_path}", False, f"Missing: {dir_path}"
                )
                self.report.add_error(f"Required directory missing: {dir_path}")

    def _check_engines(self):
        """Check engine structure"""
        engines = [
            "glb_001_market_regime",
            "glb_002_asset_impact",
            "glb_003_macro_intelligence",
        ]

        for engine in engines:
            engine_path = self.project_root / "intelligence" / "engines" / engine
            if engine_path.exists():
                engine_files = [
                    "engine.py",
                    "schemas.py",
                    "constants.py",
                    "__init__.py",
                ]
                for file in engine_files:
                    file_path = engine_path / file
                    if file_path.exists():
                        self.report.add_check(f"{engine}: {file}", True, "Exists")
                    else:
                        self.report.add_check(
                            f"{engine}: {file}", False, f"Missing: {file}"
                        )
                        self.report.add_warning(f"Missing file in {engine}: {file}")
            else:
                self.report.add_check(f"Engine: {engine}", False, "Missing")
                self.report.add_error(f"Required engine missing: {engine}")

    def _check_hub(self):
        """Check hub structure"""
        hub_path = self.project_root / "intelligence" / "hub"
        if hub_path.exists():
            required_files = ["aggregator.py", "hub.py", "__init__.py"]
            for file in required_files:
                file_path = hub_path / file
                if file_path.exists():
                    self.report.add_check(f"Hub: {file}", True, "Exists")
                else:
                    self.report.add_check(f"Hub: {file}", False, f"Missing: {file}")
                    self.report.add_warning(f"Missing hub file: {file}")
        else:
            self.report.add_check("Hub directory", False, "Missing")
            self.report.add_error("Hub directory missing")

    def _check_schemas(self):
        """Check schemas"""
        schemas_path = self.project_root / "intelligence" / "schemas"
        if schemas_path.exists():
            required_files = ["asset_impact.py", "__init__.py"]
            for file in required_files:
                file_path = schemas_path / file
                if file_path.exists():
                    self.report.add_check(f"Schemas: {file}", True, "Exists")
                else:
                    self.report.add_check(f"Schemas: {file}", False, f"Missing: {file}")
                    self.report.add_warning(f"Missing schema file: {file}")
        else:
            self.report.add_check("Schemas directory", False, "Missing")
            self.report.add_error("Schemas directory missing")


def main():
    """Main entry point"""
    logging.basicConfig(level=logging.INFO)
    logger.info("=" * 70)
    logger.info("ARC-001: ARCHITECTURE COMPLIANCE PLATFORM")
    logger.info("=" * 70)

    project_root = os.getcwd()
    logger.info(f"Project Root: {project_root}")
    logger.info("-" * 70)

    engine = ArchitectureEngine(project_root)
    report = engine.run()

    print(json.dumps(report, indent=2))

    if report["status"] == "FAILED":
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
