#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACP-001: Architecture Compliance Platform."""

import sys
from pathlib import Path
import json
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.architecture.models import ARCReport
from tools.architecture.validators.registry import get_validators

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ACP_001:
    """Architecture Compliance Platform."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.report = ARCReport()

    def run(self) -> ARCReport:
        """Run all validators."""
        logger.info("=" * 70)
        logger.info("ACP-001: ARCHITECTURE COMPLIANCE PLATFORM")
        logger.info("=" * 70)
        logger.info(f"Project Root: {self.root}")
        logger.info("-" * 70)

        validators = get_validators(self.root)
        logger.info(f"Validators: {len(validators)}")

        for validator in validators:
            name = validator.__class__.__name__
            logger.info(f"Running: {name}...")
            try:
                results = validator.validate()
                if isinstance(results, list):
                    for r in results:
                        self.report.add_result(r)
                else:
                    self.report.add_result(results)
            except Exception as e:
                logger.error(f"Validator {name} failed: {e}")
                from tools.architecture.models import ARCResult
                self.report.add_result(ARCResult(
                    validator=name,
                    passed=False,
                    message=f"Validator error: {e}",
                    severity="critical"
                ))

        self.report.calculate_score()
        self.report.is_certified()
        self._print_summary()
        return self.report

    def _print_summary(self) -> None:
        """Print the summary report."""
        print("\n" + "=" * 70)
        print("ACP-001: ARCHITECTURE COMPLIANCE REPORT")
        print("=" * 70)
        print(f"Validators: {self.report.total_validators}")
        print(f"Passed: {self.report.passed}")
        print(f"Failed: {self.report.failed}")
        print(f"Architecture Score: {self.report.architecture_score:.1f}%")
        print(f"Certified: {'✅ YES' if self.report.certified else '❌ NO'}")

        if self.report.failed > 0:
            print("\n" + "-" * 70)
            print("FAILED VALIDATIONS")
            print("-" * 70)
            for r in self.report.results:
                if not r.passed:
                    print(f"\n❌ {r.validator}")
                    print(f"   Message: {r.message}")
                    print(f"   Severity: {r.severity}")
                    if r.details:
                        print(f"   Details: {r.details}")
                    if r.suggested_fix:
                        print(f"   Suggested Fix: {r.suggested_fix}")

        print("\n" + "=" * 70)
        if self.report.certified:
            print("✅ ARCHITECTURE CERTIFIED – SAFE TO COMMIT")
        else:
            print("❌ ARCHITECTURE FAILED – FIX BEFORE COMMIT")
        print("=" * 70)

    def save_report(self, filename: str = "reports/acp_report.json") -> None:
        """Save the report to a JSON file."""
        report_path = Path(filename)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump({
                "timestamp": self.report.timestamp.isoformat(),
                "total_validators": self.report.total_validators,
                "passed": self.report.passed,
                "failed": self.report.failed,
                "critical": self.report.critical,
                "high": self.report.high,
                "medium": self.report.medium,
                "low": self.report.low,
                "architecture_score": self.report.architecture_score,
                "certified": self.report.certified,
                "results": [
                    {
                        "validator": r.validator,
                        "passed": r.passed,
                        "message": r.message,
                        "severity": r.severity,
                        "suggested_fix": r.suggested_fix,
                    }
                    for r in self.report.results
                ]
            }, f, indent=2, default=str)
        print(f"\nReport saved to: {report_path}")

def main():
    """Run ACP-001."""
    engine = ACP_001(".")
    report = engine.run()
    engine.save_report()
    sys.exit(0 if report.certified else 1)

if __name__ == "__main__":
    main()
