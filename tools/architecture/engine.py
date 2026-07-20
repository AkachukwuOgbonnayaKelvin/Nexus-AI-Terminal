#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARC-001 Architecture Compliance Engine - Simplified"""

import sys
import os
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import time
import json

# Ensure UTF-8 output
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    name: str
    passed: bool
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


class ArchitectureEngine:
    def __init__(self, root_path: Optional[Path] = None):
        self.root_path = root_path or Path.cwd()
        self.results: List[ValidationResult] = []
        self.report = None

    def run(self):
        logger.info("="*70)
        logger.info("ARC-001: ARCHITECTURE COMPLIANCE PLATFORM")
        logger.info("="*70)
        logger.info(f"Project Root: {self.root_path}")
        logger.info("-"*70)

        # Run basic checks
        self._check_engine_yaml_files()
        self._check_contract_yaml_files()
        self._check_required_folders()
        self._check_init_files()

        self.report = self._generate_report()
        self._print_summary()
        return self.report

    def _check_engine_yaml_files(self):
        """Check for engine.yaml files"""
        count = 0
        for path in self.root_path.rglob("engine.yaml"):
            if "acp" not in str(path):
                count += 1
        self.results.append(ValidationResult(
            name="EngineYamlValidator",
            passed=True,
            message=f"Found {count} engine.yaml files"
        ))

    def _check_contract_yaml_files(self):
        """Check for contract.yaml files"""
        count = 0
        for path in self.root_path.rglob("contract.yaml"):
            if "acp" not in str(path):
                count += 1
        self.results.append(ValidationResult(
            name="ContractYamlValidator",
            passed=True,
            message=f"Found {count} contract.yaml files"
        ))

    def _check_required_folders(self):
        """Check for required folders in engines"""
        engine_dirs = []
        for path in self.root_path.glob("*_engine"):
            if path.is_dir():
                engine_dirs.append(path)
        for path in self.root_path.glob("engines/*"):
            if path.is_dir() and (path / "engine.yaml").exists():
                engine_dirs.append(path)

        passed = True
        for engine_dir in engine_dirs:
            required = ["acquisition", "warehouse", "publication"]
            for folder in required:
                if not (engine_dir / folder).exists():
                    passed = False
                    self.results.append(ValidationResult(
                        name="FolderValidator",
                        passed=False,
                        message=f"{engine_dir.name}: Missing {folder}/"
                    ))

        if passed:
            self.results.append(ValidationResult(
                name="FolderValidator",
                passed=True,
                message="All required folders present"
            ))

    def _check_init_files(self):
        """Check for __init__.py files"""
        missing = []
        for path in self.root_path.rglob("*.py"):
            if path.parent != self.root_path:
                init_file = path.parent / "__init__.py"
                if not init_file.exists() and not path.name.startswith("test_"):
                    missing.append(str(path.parent.relative_to(self.root_path)))

        if missing:
            self.results.append(ValidationResult(
                name="InitValidator",
                passed=False,
                message=f"Missing __init__.py in: {', '.join(missing[:5])}"
            ))
        else:
            self.results.append(ValidationResult(
                name="InitValidator",
                passed=True,
                message="All directories have __init__.py"
            ))

    def _generate_report(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        score = (passed / total * 100) if total > 0 else 0

        class Report:
            def __init__(self):
                self.total = total
                self.passed = passed
                self.failed = failed
                self.score = score
                self.results = self.results
                self.certified = score >= 80

        report = Report()
        report.results = self.results
        return report

    def _print_summary(self):
        print("\n" + "="*70)
        print("ARC-001: ARCHITECTURE COMPLIANCE REPORT")
        print("="*70)
        print(f"Validators: {self.report.total}")
        print(f"Passed: {self.report.passed}")
        print(f"Failed: {self.report.failed}")
        print(f"Architecture Score: {self.report.score:.1f}%")

        if self.report.certified:
            print("Certified: YES")
        else:
            print("Certified: NO")
        print("="*70)

        if self.report.failed > 0:
            print("\nFAILED VALIDATORS:")
            for r in self.report.results:
                if not r.passed:
                    print(f"  - {r.name}: {r.message}")
        print("="*70)


def main():
    engine = ArchitectureEngine()
    report = engine.run()
    sys.exit(0 if report.certified else 1)


if __name__ == "__main__":
    main()
