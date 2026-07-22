#!/usr/bin/env python
"""
Autofix - Architecture auto-fix utilities.
"""

import re
from pathlib import Path


def fix_ambiguous_variable(filepath: str) -> None:
    """Fix ambiguous variable names."""
    with open(filepath, "r") as f:
        content = f.read()

    # Replace 'for l in' with 'for item in'
    content = re.sub(r"for l in", "for item in", content)

    with open(filepath, "w") as f:
        f.write(content)


def main():
    """Run autofix."""
    # Find all Python files
    for filepath in Path(".").rglob("*.py"):
        if "venv" in str(filepath) or ".mypy_cache" in str(filepath):
            continue

        with open(filepath, "r") as f:
            content = f.read()

        # Check for ambiguous variable 'l'
        if re.search(r"for l in", content):
            fix_ambiguous_variable(str(filepath))
            print(f"Fixed: {filepath}")


if __name__ == "__main__":
    main()
