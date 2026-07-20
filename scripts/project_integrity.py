#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Project Integrity Tool – Scans the entire repository for issues."""

import ast
import json
from collections import defaultdict
from typing import Dict, List, Optional, Set

import chardet
from pathlib import Path


class ProjectIntegrity:
    """Scans project for encoding, import, and structural issues."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.issues = {
            "encoding": [],
            "missing_imports": [],
            "missing_classes": [],
            "circular_imports": [],
            "broken_init": [],
            "syntax_errors": [],
            "orphan_modules": [],
            "duplicate_modules": [],
        }
        self.modules: Dict[str, Path] = {}
        self.classes: Dict[str, Set[str]] = defaultdict(set)
        self.imports: Dict[str, Set[str]] = defaultdict(set)
        self.all_exports: Set[str] = set()

    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """Read a file with automatic encoding detection."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Try to detect encoding
            try:
                with open(file_path, "rb") as f:
                    raw = f.read()
                result = chardet.detect(raw)
                encoding = result.get("encoding", "utf-8")
                confidence = result.get("confidence", 0)
                if confidence > 0.5:
                    try:
                        return raw.decode(encoding)
                    except Exception:
                        pass
            except Exception:
                pass
            # Fallback: try latin-1
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception:
                return None
        except Exception:
            return None

    def run(self) -> Dict[str, List]:
        """Run all checks."""
        self._discover_modules()
        self._check_encoding()
        self._analyze_imports()
        self._check_syntax()
        self._check_missing()
        self._check_circular()
        self._check_orphans()
        self._check_duplicates()
        self._check_broken_init()
        self._print_report()
        return self.issues

    def _discover_modules(self) -> None:
        """Discover all Python modules."""
        excluded = [
            "venv",
            "__pycache__",
            ".git",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        ]
        for py_file in self.root.rglob("*.py"):
            if any(e in str(py_file) for e in excluded):
                continue
            rel_path = py_file.relative_to(self.root)
            module_name = (
                str(rel_path).replace("\\", ".").replace("/", ".").replace(".py", "")
            )
            self.modules[module_name] = py_file
            self.all_exports.add(module_name)

    def _check_encoding(self) -> None:
        """Check all Python files for encoding issues."""
        for module_name, file_path in self.modules.items():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    f.read()
            except UnicodeDecodeError as e:
                self.issues["encoding"].append(
                    {
                        "file": str(file_path),
                        "error": str(e),
                    }
                )
                # Try to detect encoding
                try:
                    with open(file_path, "rb") as f:
                        raw = f.read()
                    result = chardet.detect(raw)
                    if result:
                        self.issues["encoding"].append(
                            {
                                "file": str(file_path),
                                "detected_encoding": result.get("encoding"),
                                "confidence": result.get("confidence"),
                            }
                        )
                except Exception:
                    pass

    def _analyze_imports(self) -> None:
        """Analyze all imports and classes."""
        for module_name, file_path in self.modules.items():
            content = self._read_file_safe(file_path)
            if not content:
                continue
            try:
                tree = ast.parse(content)

                # Find all classes
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        self.classes[module_name].add(node.name)

                # Find all imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.imports[module_name].add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            self.imports[module_name].add(node.module)
            except SyntaxError as e:
                self.issues["syntax_errors"].append(
                    {
                        "file": str(file_path),
                        "line": e.lineno,
                        "error": str(e),
                    }
                )
            except Exception:
                pass

    def _check_syntax(self) -> None:
        """Check for syntax errors."""
        for module_name, file_path in self.modules.items():
            content = self._read_file_safe(file_path)
            if not content:
                continue
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.issues["syntax_errors"].append(
                    {
                        "file": str(file_path),
                        "line": e.lineno,
                        "error": str(e),
                    }
                )

    def _check_missing(self) -> None:
        """Check for missing imports and classes."""
        stdlib = self._get_stdlib()
        for module, imported_modules in self.imports.items():
            for imp in imported_modules:
                if imp.startswith("."):
                    continue
                if imp in stdlib:
                    continue
                imp_parts = imp.split(".")
                for i in range(len(imp_parts)):
                    candidate = ".".join(imp_parts[: i + 1])
                    if candidate not in self.modules and candidate not in stdlib:
                        self.issues["missing_imports"].append(
                            {
                                "module": module,
                                "missing": candidate,
                            }
                        )
                        break

    def _get_stdlib(self) -> Set[str]:
        """Get standard library modules."""
        return {
            "typing",
            "abc",
            "asyncio",
            "datetime",
            "json",
            "pathlib",
            "os",
            "sys",
            "re",
            "collections",
            "itertools",
            "functools",
            "logging",
            "io",
            "csv",
            "xml",
            "html",
            "urllib",
            "http",
            "ssl",
            "socket",
            "hashlib",
            "base64",
            "zlib",
            "gzip",
            "zipfile",
            "tarfile",
            "shutil",
            "tempfile",
            "subprocess",
            "threading",
            "multiprocessing",
            "queue",
            "time",
            "random",
            "math",
            "decimal",
            "fractions",
            "statistics",
            "enum",
            "dataclasses",
            "contextlib",
            "importlib",
            "pkgutil",
        }

    def _check_circular(self) -> None:
        """Check for circular imports."""
        for module, deps in self.imports.items():
            for dep in deps:
                if dep in self.imports and module in self.imports[dep]:
                    self.issues["circular_imports"].append(
                        {
                            "module1": module,
                            "module2": dep,
                        }
                    )

    def _check_orphans(self) -> None:
        """Find modules that are never imported."""
        all_imported = set()
        for deps in self.imports.values():
            all_imported.update(deps)
        orphans = self.all_exports - all_imported
        for mod in orphans:
            self.issues["orphan_modules"].append(mod)

    def _check_duplicates(self) -> None:
        """Find duplicate module names."""
        seen = {}
        for module_name in self.modules:
            base = module_name.split(".")[-1]
            if base in seen:
                self.issues["duplicate_modules"].append(
                    {
                        "name": base,
                        "module1": seen[base],
                        "module2": module_name,
                    }
                )
            else:
                seen[base] = module_name

    def _check_broken_init(self) -> None:
        """Check for broken __init__.py exports."""
        for module_name, file_path in self.modules.items():
            if file_path.name == "__init__.py":
                content = self._read_file_safe(file_path)
                if not content:
                    continue
                try:
                    if "__all__" in content:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Assign):
                                for target in node.targets:
                                    if (
                                        isinstance(target, ast.Name)
                                        and target.id == "__all__"
                                    ):
                                        if isinstance(node.value, ast.List):
                                            for elt in node.value.elts:
                                                if isinstance(
                                                    elt, ast.Constant
                                                ) and isinstance(elt.value, str):
                                                    export = elt.value
                                                    export_path = (
                                                        file_path.parent
                                                        / f"{export}.py"
                                                    )
                                                    if not export_path.exists():
                                                        self.issues[
                                                            "broken_init"
                                                        ].append(
                                                            {
                                                                "file": str(file_path),
                                                                "missing_export": export,
                                                            }
                                                        )
                except Exception:
                    pass

    def _print_report(self) -> None:
        """Print the integrity report."""
        print("=" * 70)
        print("PROJECT INTEGRITY REPORT")
        print("=" * 70)

        total_issues = sum(len(v) for v in self.issues.values())
        print(f"\nTotal Modules: {len(self.modules)}")
        print(f"Total Issues Found: {total_issues}\n")

        for category, items in self.issues.items():
            if items:
                print("-" * 70)
                print(f"{category.upper().replace('_', ' ')} ({len(items)})")
                print("-" * 70)
                for item in items[:20]:
                    print(f"  {item}")
                if len(items) > 20:
                    print(f"  ... and {len(items) - 20} more")

        if total_issues == 0:
            print("\n✅ Project integrity verified! No issues found.")

        print("\n" + "=" * 70)

    def save_report(self, filename: str = "integrity_report.json") -> None:
        """Save the report to a JSON file."""
        with open(filename, "w") as f:
            json.dump(self.issues, f, indent=2, default=str)
        print(f"\nReport saved to {filename}")


if __name__ == "__main__":
    integrity = ProjectIntegrity(".")
    issues = integrity.run()
    integrity.save_report()
