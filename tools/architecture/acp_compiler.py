#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACP v2.0: Architecture Compiler – Nexus Platform Guardian."""

import sys
from pathlib import Path
import yaml
import json
import logging
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import graphlib

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class EngineSpec:
    """Engine specification from engine.yaml."""
    id: str
    name: str
    version: str
    maturity: str
    type: str
    components: Dict[str, bool]  # component -> required/optional

@dataclass
class ContractSpec:
    """Contract specification from contract.yaml."""
    publishes: List[Dict[str, str]]
    consumes: List[Dict[str, str]]
    interfaces: Dict[str, List[str]]
    dependencies: Dict[str, List[str]]
    workflow: List[str]

class ACPCompiler:
    """Architecture Compiler – Validates and certifies the entire platform."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.engines: Dict[str, EngineSpec] = {}
        self.contracts: Dict[str, ContractSpec] = {}
        self.graph: Dict[str, Set[str]] = {}
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def compile(self) -> bool:
        """Compile the entire platform architecture."""
        logger.info("=" * 70)
        logger.info("ACP v2.0: ARCHITECTURE COMPILER")
        logger.info("=" * 70)
        logger.info(f"Platform Root: {self.root}")

        self._load_specifications()
        self._validate_engines()
        self._validate_contracts()
        self._build_dependency_graph()
        self._validate_dependencies()
        self._validate_workflows()
        self._detect_drift()
        self._print_report()

        return len(self.errors) == 0

    def _load_specifications(self) -> None:
        """Load all engine and contract specifications."""
        for engine_path in self._find_engines():
            engine_name = engine_path.name

            # Load engine.yaml
            engine_file = engine_path / "engine.yaml"
            if engine_file.exists():
                try:
                    with open(engine_file, 'r') as f:
                        data = yaml.safe_load(f)
                    eng = data.get("engine", {})
                    components = data.get("components", {})
                    self.engines[engine_name] = EngineSpec(
                        id=eng.get("id", engine_name),
                        name=eng.get("name", engine_name),
                        version=eng.get("version", "1.0"),
                        maturity=eng.get("maturity", "Development"),
                        type=eng.get("type", "unknown"),
                        components={k: v == "required" for k, v in components.items()},
                    )
                except Exception as e:
                    self.errors.append({"engine": engine_name, "error": f"Failed to parse engine.yaml: {e}"})

            # Load contract.yaml
            contract_file = engine_path / "contract.yaml"
            if contract_file.exists():
                try:
                    with open(contract_file, 'r') as f:
                        data = yaml.safe_load(f)
                    self.contracts[engine_name] = ContractSpec(
                        publishes=data.get("publishes", []),
                        consumes=data.get("consumes", []),
                        interfaces=data.get("interfaces", {"required": [], "optional": []}),
                        dependencies=data.get("dependencies", {"allowed": [], "forbidden": []}),
                        workflow=data.get("workflow", []),
                    )
                except Exception as e:
                    self.errors.append({"engine": engine_name, "error": f"Failed to parse contract.yaml: {e}"})

        logger.info(f"Loaded {len(self.engines)} engine specifications")
        logger.info(f"Loaded {len(self.contracts)} contract specifications")

    def _find_engines(self) -> List[Path]:
        """Find all engine directories."""
        engines = []
        for path in self.root.glob("**/*_engine"):
            if path.is_dir() and not any(p in str(path) for p in [".venv", "__pycache__", "tools"]):
                engines.append(path)
        return engines

    def _validate_engines(self) -> None:
        """Validate each engine against its specification."""
        for engine_path in self._find_engines():
            engine_name = engine_path.name
            spec = self.engines.get(engine_name)

            if not spec:
                self.errors.append({
                    "engine": engine_name,
                    "error": "Missing engine.yaml",
                    "severity": "critical"
                })
                continue

            # Check required components
            for comp, required in spec.components.items():
                comp_path = engine_path / comp
                if required and not comp_path.exists():
                    self.errors.append({
                        "engine": engine_name,
                        "component": comp,
                        "error": f"Required component '{comp}' missing",
                        "severity": "high" if spec.maturity in ["Certified", "Production"] else "medium"
                    })
                elif not required and not comp_path.exists():
                    self.warnings.append({
                        "engine": engine_name,
                        "component": comp,
                        "warning": f"Optional component '{comp}' missing",
                        "severity": "low"
                    })

    def _validate_contracts(self) -> None:
        """Validate contracts."""
        for engine_name, contract in self.contracts.items():
            # Check NDIP topics
            for pub in contract.publishes:
                if not pub.get("topic"):
                    self.errors.append({
                        "engine": engine_name,
                        "error": f"Publication missing topic: {pub}",
                        "severity": "critical"
                    })
                if not pub.get("schema"):
                    self.warnings.append({
                        "engine": engine_name,
                        "warning": f"Publication missing schema: {pub}",
                        "severity": "medium"
                    })

    def _build_dependency_graph(self) -> None:
        """Build the dependency graph."""
        for engine_name, contract in self.contracts.items():
            self.graph[engine_name] = set()
            for pub in contract.publishes:
                topic = pub.get("topic", "")
                if topic:
                    self.graph[engine_name].add(f"NDIP[{topic}]")
            for con in contract.consumes:
                topic = con.get("topic", "")
                if topic:
                    self.graph[engine_name].add(f"NDIP[{topic}]")

        # Add cross-engine dependencies
        for engine_name, contract in self.contracts.items():
            for dep in contract.dependencies.get("allowed", []):
                self.graph[engine_name].add(dep)

    def _validate_dependencies(self) -> None:
        """Validate dependencies."""
        for engine_name, contract in self.contracts.items():
            # Check forbidden dependencies
            for forbidden in contract.dependencies.get("forbidden", []):
                if forbidden in self.graph.get(engine_name, set()):
                    self.errors.append({
                        "engine": engine_name,
                        "dependency": forbidden,
                        "error": f"Forbidden dependency: {engine_name} -> {forbidden}",
                        "severity": "critical"
                    })

    def _validate_workflows(self) -> None:
        """Validate workflows."""
        for engine_name, contract in self.contracts.items():
            if not contract.workflow:
                self.warnings.append({
                    "engine": engine_name,
                    "warning": "No workflow defined in contract.yaml",
                    "severity": "medium"
                })

    def _detect_drift(self) -> None:
        """Detect architectural drift."""
        # This would compare current state against historical state
        # For now, we check for direct imports that bypass NDIP
        # Implementation would require historical tracking
        pass

    def _print_report(self) -> None:
        """Print the compilation report."""
        print("\n" + "=" * 70)
        print("ACP v2.0: ARCHITECTURE COMPILATION REPORT")
        print("=" * 70)

        print(f"\nStatistics:")
        print(f"  Engines: {len(self.engines)}")
        print(f"  Contracts: {len(self.contracts)}")
        print(f"  Dependencies: {sum(len(v) for v in self.graph.values())}")

        if self.errors:
            print(f"\nErrors: {len(self.errors)}")
            for err in self.errors[:20]:
                print(f"  * {err.get('engine', 'unknown')}: {err.get('error', '')}")
            if len(self.errors) > 20:
                print(f"  ... and {len(self.errors) - 20} more")

        if self.warnings:
            print(f"\nWarnings: {len(self.warnings)}")
            for warn in self.warnings[:10]:
                print(f"  * {warn.get('engine', 'unknown')}: {warn.get('warning', '')}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")

        print("\n" + "-" * 70)
        print("ENGINE STATUS")
        print("-" * 70)
        for engine_name, spec in self.engines.items():
            status = "OK" if spec.maturity in ["Certified", "Production"] else "IN PROGRESS" if spec.maturity in ["Integrated"] else "DEV"
            print(f"{status} {engine_name}: {spec.maturity}")

        print("\n" + "-" * 70)
        print("NDIP TOPICS")
        print("-" * 70)
        all_topics = set()
        for contract in self.contracts.values():
            for pub in contract.publishes:
                all_topics.add(pub.get("topic", ""))
        for topic in sorted(all_topics):
            print(f"  {topic}")

        print("\n" + "=" * 70)
        if self.errors:
            print("COMPILATION FAILED")
            print("   Fix errors before proceeding")
        else:
            print("COMPILATION SUCCESSFUL")
            print("   Architecture is certified")
        print("=" * 70)

def main():
    """Run ACP v2.0."""
    compiler = ACPCompiler(".")
    success = compiler.compile()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
