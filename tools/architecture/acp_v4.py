#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACP v4.0: Architecture Operating System."""

import sys
from pathlib import Path
import yaml
import json
import logging
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class PlatformEngine:
    """Engine definition from platform registry."""

    id: str
    name: str
    path: str
    enabled: bool
    maturity: str
    type: str
    owner: str
    runtime: Dict[str, Any]
    dependencies: List[str]
    ndip: Dict[str, List[Dict[str, str]]]


@dataclass
class ArchitectureHealth:
    """Architecture health metrics."""

    architecture: float = 0.0
    runtime: float = 0.0
    ndip: float = 0.0
    warehouse: float = 0.0
    dar: float = 0.0
    testing: float = 0.0
    documentation: float = 0.0
    overall: float = 0.0


class ACPv4:
    """Architecture Operating System – Platform Compiler & Certification."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.registry: Dict[str, PlatformEngine] = {}
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
        self.suggestions: List[Dict] = []
        self.history: List[Dict] = []
        self.health = ArchitectureHealth()
        self.debt = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    def compile(self) -> bool:
        """Compile the entire platform."""
        logger.info("=" * 70)
        logger.info("ACP v4.0: ARCHITECTURE OPERATING SYSTEM")
        logger.info("=" * 70)
        logger.info(f"Platform Root: {self.root}")

        self._load_registry()
        self._validate_engines()
        self._validate_contracts()
        self._validate_dependencies()
        self._validate_ndip()
        self._validate_runtime()
        self._calculate_debt()
        self._calculate_health()
        self._detect_drift()
        self._save_history()
        self._print_report()

        return len(self.errors) == 0

    def _load_registry(self) -> None:
        """Load the platform registry."""
        registry_file = self.root / "platform_registry.yaml"
        if not registry_file.exists():
            logger.error("Platform registry not found")
            return

        try:
            with open(registry_file, "r") as f:
                data = yaml.safe_load(f)

            for eng in data.get("engines", []):
                self.registry[eng["id"]] = PlatformEngine(
                    id=eng["id"],
                    name=eng["name"],
                    path=eng["path"],
                    enabled=eng.get("enabled", True),
                    maturity=eng.get("maturity", "Development"),
                    type=eng.get("type", "unknown"),
                    owner=eng.get("owner", "unknown"),
                    runtime=eng.get("runtime", {}),
                    dependencies=eng.get("dependencies", []),
                    ndip=eng.get("ndip", {"publishes": [], "consumes": []}),
                )
            logger.info(f"Loaded {len(self.registry)} engines from registry")
        except Exception as e:
            logger.error(f"Failed to load registry: {e}")

    def _validate_engines(self) -> None:
        """Validate all registered engines."""
        for engine_id, spec in self.registry.items():
            engine_path = self.root / spec.path

            if not engine_path.exists():
                self.errors.append(
                    {
                        "engine": engine_id,
                        "path": spec.path,
                        "error": "Engine path does not exist",
                        "severity": "critical"
                        if spec.maturity in ["Production", "Certified"]
                        else "medium",
                        "fix": f"mkdir {spec.path} && touch {spec.path}/__init__.py",
                    }
                )
                continue

            # Check for engine.yaml (with explanation)
            engine_yaml = engine_path / "engine.yaml"
            if not engine_yaml.exists():
                severity = (
                    "critical"
                    if spec.maturity in ["Production", "Certified"]
                    else "high"
                )
                self.errors.append(
                    {
                        "engine": engine_id,
                        "name": spec.name,
                        "status": spec.maturity,
                        "error": "Missing engine.yaml",
                        "why": "Cannot determine engine architecture without specification",
                        "severity": severity,
                        "fix": f"acp scaffold {engine_id}",
                    }
                )

            # Check for contract.yaml
            contract_yaml = engine_path / "contract.yaml"
            if not contract_yaml.exists():
                severity = (
                    "critical"
                    if spec.maturity in ["Production", "Certified"]
                    else "high"
                )
                self.errors.append(
                    {
                        "engine": engine_id,
                        "name": spec.name,
                        "status": spec.maturity,
                        "error": "Missing contract.yaml",
                        "why": "Cannot validate NDIP contracts without specification",
                        "severity": severity,
                        "fix": f"acp scaffold {engine_id}",
                    }
                )

    def _validate_contracts(self) -> None:
        """Validate NDIP contracts."""
        for engine_id, spec in self.registry.items():
            engine_path = self.root / spec.path
            contract_file = engine_path / "contract.yaml"
            if not contract_file.exists():
                continue

            try:
                with open(contract_file, "r") as f:
                    data = yaml.safe_load(f)

                # Check for publications
                if not data.get("publishes"):
                    if spec.type == "acquisition":
                        self.warnings.append(
                            {
                                "engine": engine_id,
                                "name": spec.name,
                                "warning": "Acquisition engine has no publications",
                                "why": "Acquisition engines should publish to NDIP",
                                "severity": "medium",
                            }
                        )

                # Check for workflow
                if not data.get("workflow"):
                    self.warnings.append(
                        {
                            "engine": engine_id,
                            "name": spec.name,
                            "warning": "No workflow defined",
                            "why": "Workflow helps verify execution path",
                            "severity": "low",
                        }
                    )

                # Validate runtime configuration
                if spec.runtime.get("managed_by") == "DAR":
                    if "collect" not in str(data.get("interfaces", {})):
                        self.warnings.append(
                            {
                                "engine": engine_id,
                                "name": spec.name,
                                "warning": "DAR-managed engine missing 'collect' interface",
                                "why": "DAR needs a collect() method to execute the engine",
                                "severity": "medium",
                                "fix": "Add collect() to contract.yaml interfaces.required",
                            }
                        )

            except Exception as e:
                self.errors.append(
                    {
                        "engine": engine_id,
                        "name": spec.name,
                        "error": f"Failed to parse contract.yaml: {e}",
                        "severity": "medium",
                        "why": "Invalid YAML syntax in contract.yaml",
                        "fix": "Validate YAML syntax",
                    }
                )

    def _validate_dependencies(self) -> None:
        """Validate engine dependencies."""
        # Check if dependencies exist in registry
        for engine_id, spec in self.registry.items():
            for dep in spec.dependencies:
                if dep not in self.registry and dep not in [
                    "foundation",
                    "ndip",
                    "providers",
                    "shared_services",
                ]:
                    self.warnings.append(
                        {
                            "engine": engine_id,
                            "name": spec.name,
                            "warning": f"Unknown dependency: {dep}",
                            "why": "Dependency is not registered in the platform",
                            "severity": "medium",
                        }
                    )

    def _validate_ndip(self) -> None:
        """Validate NDIP integration."""
        for engine_id, spec in self.registry.items():
            for pub in spec.ndip.get("publishes", []):
                if not pub.get("topic"):
                    self.errors.append(
                        {
                            "engine": engine_id,
                            "name": spec.name,
                            "error": "NDIP publication missing topic",
                            "severity": "critical",
                            "why": "NDIP requires a topic for every publication",
                            "fix": "Add topic to ndip.publishes in registry",
                        }
                    )
                if not pub.get("schema"):
                    self.warnings.append(
                        {
                            "engine": engine_id,
                            "name": spec.name,
                            "warning": "NDIP publication missing schema",
                            "why": "Schema validation ensures NDIP compatibility",
                            "severity": "medium",
                            "fix": "Add schema to ndip.publishes",
                        }
                    )

    def _validate_runtime(self) -> None:
        """Validate runtime configuration."""
        for engine_id, spec in self.registry.items():
            if spec.runtime.get("managed_by") == "DAR":
                if spec.maturity in ["Production", "Certified"]:
                    # Check if engine is registered in DAR
                    dar_registry = self.root / "runtime" / "engine_registry.py"
                    if dar_registry.exists():
                        with open(dar_registry, "r") as f:
                            content = f.read()
                        if spec.id not in content and spec.name not in content:
                            self.errors.append(
                                {
                                    "engine": engine_id,
                                    "name": spec.name,
                                    "error": "DAR-managed engine not registered in DAR",
                                    "why": "DAR needs to know about this engine to schedule it",
                                    "severity": "critical",
                                    "fix": f"Add {spec.id} to runtime/engine_registry.py",
                                }
                            )

    def _calculate_debt(self) -> None:
        """Calculate weighted architecture debt."""
        for err in self.errors:
            severity = err.get("severity", "medium")
            if severity == "critical":
                self.debt["critical"] += 1
            elif severity == "high":
                self.debt["high"] += 1
            elif severity == "medium":
                self.debt["medium"] += 1
            else:
                self.debt["low"] += 1

        # Calculate weighted points (SonarQube style)
        self.debt["points"] = (
            self.debt["critical"] * 30
            + self.debt["high"] * 15
            + self.debt["medium"] * 5
            + self.debt["low"] * 1
        )
        self.debt["estimated_hours"] = self.debt["points"] / 10  # 10 points per hour

    def _calculate_health(self) -> None:
        """Calculate multidimensional health scores."""
        total_engines = len(self.registry)
        if total_engines == 0:
            return

        # Architecture score
        architecture_errors = len(
            [e for e in self.errors if e.get("severity") in ["critical", "high"]]
        )
        self.health.architecture = max(0, 100 - (architecture_errors * 5))

        # Runtime score
        runtime_engines = sum(
            1 for e in self.registry.values() if e.runtime.get("managed_by") == "DAR"
        )
        self.health.runtime = (
            (runtime_engines / total_engines) * 100 if total_engines > 0 else 0
        )

        # NDIP score
        ndip_engines = sum(1 for e in self.registry.values() if e.ndip.get("publishes"))
        self.health.ndip = (
            (ndip_engines / total_engines) * 100 if total_engines > 0 else 0
        )

        # Warehouse score
        warehouse_engines = sum(
            1
            for e_id, spec in self.registry.items()
            if (self.root / spec.path / "warehouse").exists()
        )
        self.health.warehouse = (
            (warehouse_engines / total_engines) * 100 if total_engines > 0 else 0
        )

        # DAR score
        self.health.dar = 0 if len(self.errors) > 0 else 100

        # Testing score
        test_engines = sum(
            1
            for e_id, spec in self.registry.items()
            if (self.root / spec.path / "tests").exists()
        )
        self.health.testing = (
            (test_engines / total_engines) * 100 if total_engines > 0 else 0
        )

        # Documentation score
        doc_engines = sum(
            1
            for e_id, spec in self.registry.items()
            if (self.root / spec.path / "README.md").exists()
        )
        self.health.documentation = (
            (doc_engines / total_engines) * 100 if total_engines > 0 else 0
        )

        # Overall
        scores = [
            self.health.architecture,
            self.health.runtime,
            self.health.ndip,
            self.health.warehouse,
            self.health.dar,
            self.health.testing,
            self.health.documentation,
        ]
        self.health.overall = sum(scores) / len(scores)

    def _detect_drift(self) -> None:
        """Detect architectural drift."""
        history_file = self.root / "data" / "architecture_history.json"
        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    history = json.load(f)
                if history:
                    last = history[-1].get("overall", 0)
                    if self.health.overall < last - 5:
                        self.warnings.append(
                            {
                                "engine": "platform",
                                "name": "Platform",
                                "warning": f"Architectural drift detected: {last:.1f}% -> {self.health.overall:.1f}%",
                                "why": "Platform health has decreased significantly",
                                "severity": "high",
                            }
                        )
            except Exception:
                pass

    def _save_history(self) -> None:
        """Save architecture history."""
        history_dir = self.root / "data"
        history_dir.mkdir(parents=True, exist_ok=True)
        history_file = history_dir / "architecture_history.json"

        history = []
        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    history = json.load(f)
            except Exception:
                pass

        history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "overall": self.health.overall,
                "architecture": self.health.architecture,
                "runtime": self.health.runtime,
                "ndip": self.health.ndip,
                "warehouse": self.health.warehouse,
                "dar": self.health.dar,
                "testing": self.health.testing,
                "documentation": self.health.documentation,
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            }
        )

        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)

    def _print_report(self) -> None:
        """Print the compilation report."""
        print("\n" + "=" * 70)
        print("ACP v4.0: ARCHITECTURE OPERATING SYSTEM REPORT")
        print("=" * 70)

        # Platform Overview
        print("\nPlatform Overview:")
        print(f"  Registered Engines: {len(self.registry)}")
        enabled = sum(1 for e in self.registry.values() if e.enabled)
        print(f"  Enabled Engines: {enabled}")
        production = sum(
            1
            for e in self.registry.values()
            if e.maturity in ["Production", "Certified"]
        )
        print(f"  Production Engines: {production}")

        # Health Scores
        print("\n" + "-" * 70)
        print("Architecture Health")
        print("-" * 70)
        print(f"  Architecture: {self.health.architecture:.1f}%")
        print(f"  Runtime (DAR): {self.health.runtime:.1f}%")
        print(f"  NDIP: {self.health.ndip:.1f}%")
        print(f"  Warehouse: {self.health.warehouse:.1f}%")
        print(f"  DAR: {self.health.dar:.1f}%")
        print(f"  Testing: {self.health.testing:.1f}%")
        print(f"  Documentation: {self.health.documentation:.1f}%")
        print(f"  Overall: {self.health.overall:.1f}%")

        # Engine Status
        print("\n" + "-" * 70)
        print("Engine Status")
        print("-" * 70)
        for engine_id, spec in self.registry.items():
            status = (
                "OK"
                if spec.maturity in ["Production", "Certified"]
                else "IN PROGRESS"
                if spec.maturity in ["Integrated"]
                else "DEV"
            )
            enabled = "Enabled" if spec.enabled else "Disabled"
            print(f"  {status} {engine_id}: {spec.name} ({spec.maturity}) [{enabled}]")

        # Architecture Debt
        print("\n" + "-" * 70)
        print("Architecture Debt")
        print("-" * 70)
        print(f"  Critical: {self.debt['critical']}")
        print(f"  High: {self.debt['high']}")
        print(f"  Medium: {self.debt['medium']}")
        print(f"  Low: {self.debt['low']}")
        print(f"  Debt Points: {self.debt.get('points', 0)}")
        print(f"  Estimated Fix Time: {self.debt.get('estimated_hours', 0):.1f} hours")

        # Errors
        if self.errors:
            print("\n" + "-" * 70)
            print(f"Errors ({len(self.errors)})")
            print("-" * 70)
            for err in self.errors[:10]:
                print(f"\n  * {err.get('engine', 'unknown')}: {err.get('name', '')}")
                print(f"    Error: {err.get('error', '')}")
                if err.get("why"):
                    print(f"    Why: {err['why']}")
                if err.get("fix"):
                    print(f"    Fix: {err['fix']}")
            if len(self.errors) > 10:
                print(f"\n  ... and {len(self.errors) - 10} more")

        # Warnings
        if self.warnings:
            print("\n" + "-" * 70)
            print(f"Warnings ({len(self.warnings)})")
            print("-" * 70)
            for warn in self.warnings[:5]:
                print(f"\n  * {warn.get('engine', 'unknown')}: {warn.get('name', '')}")
                print(f"    Warning: {warn.get('warning', '')}")
                if warn.get("why"):
                    print(f"    Why: {warn['why']}")
                if warn.get("fix"):
                    print(f"    Fix: {warn['fix']}")
            if len(self.warnings) > 5:
                print(f"\n  ... and {len(self.warnings) - 5} more")

        # Platform Readiness
        print("\n" + "-" * 70)
        print("Platform Readiness")
        print("-" * 70)
        readiness = (
            "100% - Fully Certified"
            if self.health.overall >= 95
            else "90% - Production Ready"
            if self.health.overall >= 80
            else "75% - Near Production"
            if self.health.overall >= 65
            else "50% - In Development"
            if self.health.overall >= 50
            else "25% - Early Stage"
            if self.health.overall >= 25
            else "10% - Initial Setup"
        )
        print(f"  Readiness: {readiness}")

        # Build Gate
        print("\n" + "=" * 70)
        if self.errors:
            print("BUILD GATE: BLOCKED")
            print("   Fix errors before merging")
        else:
            print("BUILD GATE: PASSED")
            print("   Platform is certified")
        print("=" * 70)


def main():
    """Run ACP v4.0."""
    acp = ACPv4(".")
    success = acp.compile()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
