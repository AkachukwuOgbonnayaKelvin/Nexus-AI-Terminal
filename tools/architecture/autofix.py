#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARC-002: Architecture Auto-Fixer – Automatically fixes common issues."""

from pathlib import Path
from typing import List, Tuple


class AutoFixer:
    """Automatically fixes architecture issues."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.fixes: List[Tuple[Path, str, str]] = []
        self.fixed: List[str] = []

    def run(self) -> bool:
        """Run all auto-fixes."""
        print("=" * 70)
        print("ARC-002: ARCHITECTURE AUTO-FIXER")
        print("=" * 70)
        print(f"Scanning: {self.root / 'tools/architecture'}")
        print("-" * 70)

        self._fix_engine_imports()
        self._fix_models_imports()
        self._fix_validator_inheritance()
        self._fix_registry_imports()

        self._apply_fixes()
        self._print_report()
        return len(self.fixes) == 0

    def _fix_engine_imports(self) -> None:
        """Fix imports from engine.py to models.py."""
        for py_file in (self.root / "tools" / "architecture").rglob("*.py"):
            if any(
                e in str(py_file)
                for e in ["__pycache__", ".venv", "bootstrap_check.py", "autofix.py"]
            ):
                continue
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                new_content = content
                if "from tools.architecture.engine import" in content:
                    new_content = content.replace(
                        "from tools.architecture.engine import",
                        "from tools.architecture.models import",
                    )
                    if new_content != content:
                        self.fixes.append(
                            (py_file, "import", "from engine.py → models.py")
                        )
                if "from ..engine import" in content:
                    new_content = content.replace(
                        "from ..engine import", "from tools.architecture.models import"
                    )
                    if new_content != content:
                        self.fixes.append(
                            (py_file, "import", "from ..engine → models.py")
                        )
                if new_content != content:
                    py_file.write_text(new_content, encoding="utf-8")
            except Exception:
                pass

    def _fix_models_imports(self) -> None:
        """Add missing models.py imports."""
        for py_file in (self.root / "tools" / "architecture" / "validators").glob(
            "*.py"
        ):
            if py_file.name in ["__init__.py", "base.py", "registry.py"]:
                continue
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                if (
                    "ARCResult" in content
                    and "from tools.architecture.models import ARCResult" not in content
                ):
                    if "from .base import" not in content:
                        new_content = (
                            "from tools.architecture.models import ARCResult\n"
                            + content
                        )
                        self.fixes.append(
                            (py_file, "import", "Added ARCResult import from models.py")
                        )
                        py_file.write_text(new_content, encoding="utf-8")
            except Exception:
                pass

    def _fix_validator_inheritance(self) -> None:
        """Fix validators to inherit from BaseValidator."""
        for py_file in (self.root / "tools" / "architecture" / "validators").glob(
            "*.py"
        ):
            if py_file.name in ["__init__.py", "base.py", "registry.py"]:
                continue
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                if "class " in content and "Validator" in py_file.name:
                    if "BaseValidator" not in content:
                        # Add BaseValidator import and inheritance
                        lines = content.split("\n")
                        new_lines = []
                        for line in lines:
                            if (
                                line.strip().startswith("class ")
                                and "Validator" in line
                                and "(" not in line
                            ):
                                line = (
                                    line.replace("class ", "class ") + "(BaseValidator)"
                                )
                            new_lines.append(line)
                        if not any(
                            "from tools.architecture.validators.base import BaseValidator"
                            in l
                            for l in new_lines
                        ):
                            new_lines.insert(
                                0,
                                "from tools.architecture.validators.base import BaseValidator",
                            )
                        new_content = "\n".join(new_lines)
                        if new_content != content:
                            self.fixes.append(
                                (
                                    py_file,
                                    "inheritance",
                                    "Added BaseValidator inheritance",
                                )
                            )
                            py_file.write_text(new_content, encoding="utf-8")
            except Exception:
                pass

    def _fix_registry_imports(self) -> None:
        """Fix registry.py imports."""
        registry_file = (
            self.root / "tools" / "architecture" / "validators" / "registry.py"
        )
        if not registry_file.exists():
            return
        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                content = f.read()
            if "from tools.architecture.engine import" in content:
                new_content = content.replace(
                    "from tools.architecture.engine import",
                    "from tools.architecture.models import",
                )
                self.fixes.append(
                    (registry_file, "import", "Fixed registry engine import")
                )
                registry_file.write_text(new_content, encoding="utf-8")
        except Exception:
            pass

    def _apply_fixes(self) -> None:
        """Apply all fixes (already applied inline)."""
        pass

    def _print_report(self) -> None:
        """Print the fix report."""
        print("\n" + "=" * 70)
        print("AUTO-FIX REPORT")
        print("=" * 70)

        if self.fixes:
            print(f"\n✅ Applied {len(self.fixes)} fixes:")
            for file, fix_type, message in self.fixes:
                print(f"  {file.relative_to(self.root)}: {message}")
        else:
            print("\n✅ No fixes needed")

        print("=" * 70)


def main():
    """Run the auto-fixer."""
    fixer = AutoFixer(".")
    fixer.run()


if __name__ == "__main__":
    main()
