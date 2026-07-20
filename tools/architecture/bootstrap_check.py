#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bootstrap Check - Validates ACP can run before any compilation
"""

import sys
from pathlib import Path


def check_acp_structure():
    """Check that ACP has the required structure"""
    errors = []
    warnings = []

    # Required directories
    required_dirs = ["acp", "acp/core", "acp/compilers", "acp/output", "engines"]

    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            errors.append(f"Missing directory: {dir_path}")
        elif not Path(dir_path).is_dir():
            errors.append(f"Not a directory: {dir_path}")

    # Required files
    required_files = [
        "acp/__init__.py",
        "acp/core/__init__.py",
        "acp/core/architecture_os.py",
        "acp/compilers/__init__.py",
        "acp/output/__init__.py",
        "acp/output/visualizer.py",
        "acp/acp.py",
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Missing file: {file_path}")

    return errors, warnings


def main():
    print("\n" + "=" * 50)
    print("  ACP BOOTSTRAP CHECK")
    print("=" * 50)

    errors, warnings = check_acp_structure()

    if errors:
        print("\n[ERROR] Critical issues found:")
        for error in errors:
            print(f"  - {error}")
        print("\n[FAIL] Bootstrap check failed")
        sys.exit(1)
    else:
        print("\n[OK] All required files and directories present")

        if warnings:
            print("\n[WARN] Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        print("\n[PASS] Bootstrap check passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
