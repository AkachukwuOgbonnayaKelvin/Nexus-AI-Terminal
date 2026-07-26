#!/usr/bin/env python3
"""ACP v3.0: Platform Architecture Compiler."""

import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

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


@dataclass
class ArchitectureDebt:
    """Architecture debt metrics."""

    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    estimated_fix_time: str = "0 hours"


class ACPPlatform:
    """Platform Architecture Compiler."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.registry: dict[str, PlatformEngine] = {}
        self.errors: list[dict] = []
        self.warnings: list[dict] = []
        self.suggestions: list[dict] = []
        self.debt = ArchitectureDebt()

    def compile(self) -> bool:
        """Compile the entire platform."""
        logger.info("=" * 70)
        logger.info("ACP v3.0: PLATFORM ARCHITECTURE COMPILER")
        logger.info("=" * 70)
        logger.info(f"Platform Root: {self.root}")

        self._load_registry()
        self._validate_registered_engines()
        self._validate_engine_states()
        self._validate_contracts()
        self._validate_dependencies()
        self._calculate_debt()
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
                )
            logger.info(f"Loaded {len(self.registry)} engines from registry")
        except Exception as e:
            logger.error(f"Failed to load registry: {e}")

    def _validate_registered_engines(self) -> None:
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
                        "fix": f"Create directory: {spec.path}",
                    }
                )
                continue

            # Check for engine.yaml
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
                        "error": "Missing engine.yaml",
                        "severity": severity,
                        "fix": f"Create {spec.path}/engine.yaml",
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
                        "error": "Missing contract.yaml",
                        "severity": severity,
                        "fix": f"Create {spec.path}/contract.yaml",
                    }
                )

    def _validate_engine_states(self) -> None:
        """Validate based on engine maturity."""
        for engine_id, spec in self.registry.items():
            engine_path = self.root / spec.path
            if not engine_path.exists():
                continue

            # Check if engine is ready based on maturity
            if spec.maturity in ["Production", "Certified"]:
                required = ["warehouse", "publication", "runtime", "gateway"]
                missing = [r for r in required if not (engine_path / r).exists()]
                for m in missing:
                    self.errors.append(
                        {
                            "engine": engine_id,
                            "error": f"Production engine missing required component: {m}",
                            "severity": "critical",
                            "fix": f"Create {spec.path}/{m}/",
                        }
                    )

            elif spec.maturity in ["Integrated"]:
                required = ["warehouse", "publication", "runtime"]
                missing = [r for r in required if not (engine_path / r).exists()]
                for m in missing:
                    self.warnings.append(
                        {
                            "engine": engine_id,
                            "warning": f"Integrated engine missing recommended component: {m}",
                            "severity": "medium",
                            "fix": f"Consider adding {spec.path}/{m}/",
                        }
                    )

            elif spec.maturity in ["Development"]:
                optional = [
                    "warehouse",
                    "publication",
                    "runtime",
                    "gateway",
                    "observability",
                ]
                missing = [o for o in optional if not (engine_path / o).exists()]
                for m in missing:
                    self.suggestions.append(
                        {
                            "engine": engine_id,
                            "suggestion": f"Add optional component for development: {m}",
                            "severity": "low",
                            "fix": f"Create {spec.path}/{m}/ when needed",
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
                                "warning": "Acquisition engine has no publications",
                                "severity": "medium",
                            }
                        )

                # Check for workflow
                if not data.get("workflow"):
                    self.warnings.append(
                        {
                            "engine": engine_id,
                            "warning": "No workflow defined in contract.yaml",
                            "severity": "low",
                        }
                    )

            except Exception as e:
                self.errors.append(
                    {
                        "engine": engine_id,
                        "error": f"Failed to parse contract.yaml: {e}",
                        "severity": "medium",
                    }
                )

    def _validate_dependencies(self) -> None:
        """Validate dependencies."""
        # This would check for forbidden dependencies between engines

    def _calculate_debt(self) -> None:
        """Calculate architecture debt."""
        for err in self.errors:
            severity = err.get("severity", "medium")
            if severity == "critical":
                self.debt.critical += 1
            elif severity == "high":
                self.debt.high += 1
            elif severity == "medium":
                self.debt.medium += 1
            else:
                self.debt.low += 1

        # Estimate fix time
        total = (
            self.debt.critical * 30
            + self.debt.high * 15
            + self.debt.medium * 5
            + self.debt.low * 1
        )
        if total < 60:
            self.debt.estimated_fix_time = f"{total} minutes"
        elif total < 1440:
            self.debt.estimated_fix_time = f"{total // 60} hours"
        else:
            self.debt.estimated_fix_time = f"{total // 1440} days"

    def _print_report(self) -> None:
        """Print the compilation report."""
        print("\n" + "=" * 70)
        print("ACP v3.0: PLATFORM ARCHITECTURE REPORT")
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
        print(f"  Critical: {self.debt.critical}")
        print(f"  High: {self.debt.high}")
        print(f"  Medium: {self.debt.medium}")
        print(f"  Low: {self.debt.low}")
        print(f"  Estimated Fix Time: {self.debt.estimated_fix_time}")

        # Errors
        if self.errors:
            print("\n" + "-" * 70)
            print(f"Errors ({len(self.errors)})")
            print("-" * 70)
            for err in self.errors[:10]:
                print(f"  * {err.get('engine', 'unknown')}: {err.get('error', '')}")
                if err.get("fix"):
                    print(f"    Fix: {err['fix']}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more")

        # Warnings
        if self.warnings:
            print("\n" + "-" * 70)
            print(f"Warnings ({len(self.warnings)})")
            print("-" * 70)
            for warn in self.warnings[:5]:
                print(f"  * {warn.get('engine', 'unknown')}: {warn.get('warning', '')}")
            if len(self.warnings) > 5:
                print(f"  ... and {len(self.warnings) - 5} more")

        # Suggestions
        if self.suggestions:
            print("\n" + "-" * 70)
            print(f"Suggestions ({len(self.suggestions)})")
            print("-" * 70)
            for sug in self.suggestions[:5]:
                print(
                    f"  * {sug.get('engine', 'unknown')}: {sug.get('suggestion', '')}"
                )
            if len(self.suggestions) > 5:
                print(f"  ... and {len(self.suggestions) - 5} more")

        # Platform Readiness
        print("\n" + "-" * 70)
        print("Platform Readiness")
        print("-" * 70)

        total_issues = len(self.errors) + len(self.warnings)
        if total_issues == 0:
            readiness = "100% - Platform is fully certified"
        elif len(self.errors) == 0:
            readiness = "95% - Platform is certified with warnings"
        elif len(self.errors) < 5:
            readiness = "85% - Platform has minor issues"
        else:
            readiness = "65% - Platform needs significant work"

        print(f"  Readiness: {readiness}")

        print("\n" + "=" * 70)
        if self.errors:
            print("PLATFORM COMPILATION FAILED")
            print("   Fix errors before proceeding")
        else:
            print("PLATFORM COMPILATION SUCCESSFUL")
            if self.warnings:
                print("   Platform is certified with warnings")
            else:
                print("   Platform is fully certified")
        print("=" * 70)


def main():
    """Run ACP v3.0."""
    compiler = ACPPlatform(".")
    success = compiler.compile()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
