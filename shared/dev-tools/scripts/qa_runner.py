#!/usr/bin/env python3
"""
NAQAP QA Runner for Nexus AI Terminal
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run_qa() -> bool:
    """Run all QA checks."""
    print("=" * 60)
    print("RUNNING QA CHECKS")
    print("=" * 60)

    checks = [
        (["ruff", "check", str(ROOT)], "Ruff Linting & Imports"),
        (["ruff", "format", "--check", str(ROOT)], "Ruff Formatting"),
        (["mypy", "--ignore-missing-imports", str(ROOT)], "Type Checking"),
        (["pytest", "--tb=short", "--collect-only"], "Test Collection"),
    ]

    all_passed: bool = True

    for cmd, name in checks:
        print(f"\nRunning: {name}")
        print("-" * 40)

        try:
            result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"PASSED: {name}")
            else:
                print(f"FAILED: {name}")
                if result.stdout:
                    print(result.stdout[:500])
                if result.stderr:
                    print(result.stderr[:500])
                all_passed = False
        except Exception as e:
            print(f"ERROR: {name} - {e}")
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    sys.exit(0 if run_qa() else 1)
