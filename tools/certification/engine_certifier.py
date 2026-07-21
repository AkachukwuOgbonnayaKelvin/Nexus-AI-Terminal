#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nexus AI Terminal - Unified Engine Certification System

Certifies all Global Intelligence engines (GLB-001 through GLB-006)
against canonical standards.
"""

import sys
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# ============================================================
# Bootstrap project root
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class CertStatus(str, Enum):
    """Certification status"""

    CERTIFIED = "CERTIFIED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    NOT_EVALUATED = "NOT_EVALUATED"


@dataclass
class CertificationResult:
    """Result of a certification check"""

    name: str
    status: CertStatus
    score: float = 0.0
    details: str = ""
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class EngineCertification:
    """Full certification result for an engine"""

    engine_id: str
    engine_name: str
    status: CertStatus
    overall_score: float
    results: List[CertificationResult]
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class EngineCertifier:
    """Certifies Global Intelligence engines"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

        # Engine paths
        self.engine_paths = {
            "GLB-001": "intelligence/engines/glb_001_market_regime",
            "GLB-002": "intelligence/engines/glb_002_asset_impact",
            "GLB-003": "intelligence/engines/glb_003_macro_intelligence",
            "GLB-004": "intelligence/engines/glb_004_economic_events",
            "GLB-005": "intelligence/engines/glb_005_central_bank",
            "GLB-006": "intelligence/engines/glb_006_geopolitical_risk",
        }

        self.engine_modules = {
            "GLB-001": "intelligence.engines.glb_001_market_regime",
            "GLB-002": "intelligence.engines.glb_002_asset_impact",
            "GLB-003": "intelligence.engines.glb_003_macro_intelligence",
            "GLB-004": "intelligence.engines.glb_004_economic_events",
            "GLB-005": "intelligence.engines.glb_005_central_bank",
            "GLB-006": "intelligence.engines.glb_006_geopolitical_risk",
        }

        self.engine_classes = {
            "GLB-001": "MarketRegimeEngine",
            "GLB-002": "AssetImpactEngine",
            "GLB-003": "MacroIntelligenceEngine",
            "GLB-004": "EconomicEventsEngine",
            "GLB-005": "CentralBankEngine",
            "GLB-006": "GeopoliticalRiskEngine",
        }

        # Architecture profiles for different engine layouts
        self.architecture_profiles = {
            # Flat structure (GLB-001, GLB-002, GLB-003)
            "profile_a": {
                "required_files": [
                    "__init__.py",
                    "constants.py",
                    "schemas.py",
                    "engine.py",
                ],
                "required_dirs": [],
                "optional_files": ["asset_impact_matrix.py"],
            },
            # Subdirectory structure (GLB-004)
            "profile_b": {
                "required_files": [
                    "__init__.py",
                    "constants.py",
                    "engine.py",
                ],
                "required_dirs": [
                    "input/",
                    "analysis/",
                    "impact/",
                ],
                "optional_files": ["asset_impact_matrix.py", "schemas.py"],
            },
            # Full subdirectory structure (GLB-005, GLB-006)
            "profile_c": {
                "required_files": [
                    "__init__.py",
                    "constants.py",
                    "engine.py",
                ],
                "required_dirs": [
                    "input/",
                    "analysis/",
                    "transmission/",
                    "impact/",
                ],
                "optional_files": ["asset_impact_matrix.py", "schemas.py"],
            },
        }

        self.engine_profiles = {
            "GLB-001": "profile_a",
            "GLB-002": "profile_a",
            "GLB-003": "profile_a",
            "GLB-004": "profile_b",
            "GLB-005": "profile_c",
            "GLB-006": "profile_c",
        }

    def certify_engine(self, engine_id: str) -> EngineCertification:
        """Certify a single engine"""
        print(f"\n{'=' * 70}")
        print(f"CERTIFYING {engine_id}")
        print(f"{'=' * 70}")

        results = []
        overall_score = 0.0
        total_weight = 0.0
        blocked = False

        # 1. Structural Certification
        structural = self._check_structure(engine_id)
        results.append(structural)
        if structural.status == CertStatus.BLOCKED:
            blocked = True
        overall_score += structural.score * 0.15
        total_weight += 0.15

        # 2. Import Certification
        import_check = self._check_imports(engine_id)
        results.append(import_check)
        if import_check.status == CertStatus.BLOCKED:
            blocked = True
        overall_score += import_check.score * 0.15
        total_weight += 0.15

        # 3. Engine Class Certification
        class_check = self._check_engine_class(engine_id)
        results.append(class_check)
        overall_score += class_check.score * 0.15
        total_weight += 0.15

        # 4. Method Certification
        method_check = self._check_methods(engine_id)
        results.append(method_check)
        overall_score += method_check.score * 0.15
        total_weight += 0.15

        # 5. Schema Certification
        schema_check = self._check_schemas(engine_id)
        results.append(schema_check)
        overall_score += schema_check.score * 0.15
        total_weight += 0.15

        # 6. Asset Impact Matrix Certification
        aim_check = self._check_asset_impact_matrix(engine_id)
        results.append(aim_check)
        overall_score += aim_check.score * 0.15
        total_weight += 0.15

        # 7. Integration Certification
        integration_check = self._check_integration(engine_id)
        results.append(integration_check)
        overall_score += integration_check.score * 0.10
        total_weight += 0.10

        # Calculate final score
        if total_weight > 0:
            final_score = overall_score / total_weight
        else:
            final_score = 0.0

        # Determine status
        if blocked:
            status = CertStatus.BLOCKED
        elif final_score >= 85:
            status = CertStatus.CERTIFIED
        elif final_score >= 60:
            status = CertStatus.PARTIAL
        else:
            status = CertStatus.FAILED

        return EngineCertification(
            engine_id=engine_id,
            engine_name=self.engine_paths.get(engine_id, engine_id),
            status=status,
            overall_score=final_score,
            results=results,
            timestamp=datetime.utcnow().isoformat(),
            metadata={"version": "1.0.0"},
        )

    def _check_structure(self, engine_id: str) -> CertificationResult:
        """Check engine directory structure using architecture profile"""
        path = self.engine_paths.get(engine_id)
        if not path:
            return CertificationResult(
                name="Structural",
                status=CertStatus.FAILED,
                score=0,
                details=f"Engine path not found for {engine_id}",
                errors=[f"Unknown engine: {engine_id}"],
            )

        engine_dir = self.project_root / path
        if not engine_dir.exists():
            return CertificationResult(
                name="Structural",
                status=CertStatus.FAILED,
                score=0,
                details=f"Engine directory not found: {engine_dir}",
                errors=[f"Missing engine directory: {engine_dir}"],
            )

        # Get profile for this engine
        profile_name = self.engine_profiles.get(engine_id, "profile_a")
        profile = self.architecture_profiles.get(
            profile_name, self.architecture_profiles["profile_a"]
        )

        missing_files = []
        for file in profile.get("required_files", []):
            if not (engine_dir / file).exists():
                missing_files.append(file)

        missing_dirs = []
        for dir_path in profile.get("required_dirs", []):
            if not (engine_dir / dir_path).exists():
                missing_dirs.append(dir_path)

        if missing_files or missing_dirs:
            details = []
            if missing_files:
                details.append(f"Missing files: {', '.join(missing_files)}")
            if missing_dirs:
                details.append(f"Missing dirs: {', '.join(missing_dirs)}")

            return CertificationResult(
                name="Structural",
                status=CertStatus.PARTIAL,
                score=70.0,
                details="; ".join(details),
                errors=[f"Missing required structure: {'; '.join(details)}"],
            )

        return CertificationResult(
            name="Structural",
            status=CertStatus.CERTIFIED,
            score=100.0,
            details="All required files and directories present",
        )

    def _check_imports(self, engine_id: str) -> CertificationResult:
        """Check if engine imports correctly"""
        module_path = self.engine_modules.get(engine_id)
        if not module_path:
            return CertificationResult(
                name="Imports",
                status=CertStatus.FAILED,
                score=0,
                details=f"Module path not found for {engine_id}",
                errors=[f"Unknown engine: {engine_id}"],
            )

        try:
            importlib.import_module(f"{module_path}.engine")
            return CertificationResult(
                name="Imports",
                status=CertStatus.CERTIFIED,
                score=100.0,
                details="Engine imports successfully",
            )
        except ImportError as e:
            if "No module named 'intelligence'" in str(e):
                return CertificationResult(
                    name="Imports",
                    status=CertStatus.BLOCKED,
                    score=0,
                    details="Project import bootstrap failure - check PYTHONPATH",
                    errors=[str(e)],
                )
            return CertificationResult(
                name="Imports",
                status=CertStatus.FAILED,
                score=0,
                details=f"Import failed: {e}",
                errors=[str(e)],
            )
        except Exception as e:
            return CertificationResult(
                name="Imports",
                status=CertStatus.FAILED,
                score=0,
                details=f"Import failed: {e}",
                errors=[str(e)],
            )

    def _check_engine_class(self, engine_id: str) -> CertificationResult:
        """Check if engine class exists and has correct structure"""
        module_path = self.engine_modules.get(engine_id)
        class_name = self.engine_classes.get(engine_id)

        if not module_path or not class_name:
            return CertificationResult(
                name="Engine Class",
                status=CertStatus.FAILED,
                score=0,
                details="Engine class not found",
                errors=["Unknown engine or class"],
            )

        try:
            module = importlib.import_module(f"{module_path}.engine")
            engine_class = getattr(module, class_name, None)

            if engine_class is None:
                return CertificationResult(
                    name="Engine Class",
                    status=CertStatus.FAILED,
                    score=0,
                    details=f"Class {class_name} not found",
                    errors=[f"Missing class: {class_name}"],
                )

            # Check methods
            methods = ["run", "consume_ndip", "health_check"]
            missing_methods = []
            for method in methods:
                if not hasattr(engine_class, method):
                    missing_methods.append(method)

            if missing_methods:
                return CertificationResult(
                    name="Engine Class",
                    status=CertStatus.PARTIAL,
                    score=70.0,
                    details=f"Missing methods: {', '.join(missing_methods)}",
                    errors=[f"Missing required methods: {', '.join(missing_methods)}"],
                )

            return CertificationResult(
                name="Engine Class",
                status=CertStatus.CERTIFIED,
                score=100.0,
                details="Engine class correctly structured",
            )

        except ImportError as e:
            if "No module named 'intelligence'" in str(e):
                return CertificationResult(
                    name="Engine Class",
                    status=CertStatus.BLOCKED,
                    score=0,
                    details="Project import bootstrap failure",
                    errors=[str(e)],
                )
            return CertificationResult(
                name="Engine Class",
                status=CertStatus.FAILED,
                score=0,
                details=f"Engine class check failed: {e}",
                errors=[str(e)],
            )
        except Exception as e:
            return CertificationResult(
                name="Engine Class",
                status=CertStatus.FAILED,
                score=0,
                details=f"Engine class check failed: {e}",
                errors=[str(e)],
            )

    def _check_methods(self, engine_id: str) -> CertificationResult:
        """Check if engine methods are correctly implemented"""
        module_path = self.engine_modules.get(engine_id)
        class_name = self.engine_classes.get(engine_id)

        if not module_path or not class_name:
            return CertificationResult(
                name="Methods",
                status=CertStatus.FAILED,
                score=0,
                details="Engine class not found",
                errors=["Unknown engine or class"],
            )

        try:
            module = importlib.import_module(f"{module_path}.engine")
            engine_class = getattr(module, class_name)

            # Check method signatures
            method_checks = []

            # run() should exist
            if hasattr(engine_class, "run"):
                run_method = getattr(engine_class, "run")
                sig = inspect.signature(run_method)
                if len(sig.parameters) == 1:  # self only
                    method_checks.append(True)
                else:
                    method_checks.append(False)
            else:
                method_checks.append(False)

            # consume_ndip() should exist
            if hasattr(engine_class, "consume_ndip"):
                method_checks.append(True)
            else:
                method_checks.append(False)

            # health_check() should exist
            if hasattr(engine_class, "health_check"):
                method_checks.append(True)
            else:
                method_checks.append(False)

            # Check for get_last_report() for newer engines
            if engine_id in ["GLB-004", "GLB-005", "GLB-006"]:
                if hasattr(engine_class, "get_last_report"):
                    method_checks.append(True)
                else:
                    method_checks.append(False)

            passed_checks = sum(method_checks)
            total_checks = len(method_checks)
            score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0

            if score == 100:
                return CertificationResult(
                    name="Methods",
                    status=CertStatus.CERTIFIED,
                    score=100.0,
                    details="All methods correctly implemented",
                )
            else:
                return CertificationResult(
                    name="Methods",
                    status=CertStatus.PARTIAL,
                    score=score,
                    details=f"{passed_checks}/{total_checks} methods correct",
                    errors=["Method signature issues detected"],
                )

        except ImportError as e:
            if "No module named 'intelligence'" in str(e):
                return CertificationResult(
                    name="Methods",
                    status=CertStatus.BLOCKED,
                    score=0,
                    details="Project import bootstrap failure",
                    errors=[str(e)],
                )
            return CertificationResult(
                name="Methods",
                status=CertStatus.FAILED,
                score=0,
                details=f"Method check failed: {e}",
                errors=[str(e)],
            )
        except Exception as e:
            return CertificationResult(
                name="Methods",
                status=CertStatus.FAILED,
                score=0,
                details=f"Method check failed: {e}",
                errors=[str(e)],
            )

    def _check_schemas(self, engine_id: str) -> CertificationResult:
        """Check if schemas are correctly defined"""
        module_path = self.engine_modules.get(engine_id)

        if not module_path:
            return CertificationResult(
                name="Schemas",
                status=CertStatus.FAILED,
                score=0,
                details="Module path not found",
                errors=["Unknown engine"],
            )

        # For engines with subdirectory structure, try both locations
        schema_locations = [
            f"{module_path}.schemas",
            f"{module_path}.input.schemas",
        ]

        found_schemas = []
        for loc in schema_locations:
            try:
                schemas_module = importlib.import_module(loc)
                if hasattr(schemas_module, "AssetImpactMatrix"):
                    found_schemas.append("AssetImpactMatrix")
                if hasattr(schemas_module, "RegimeReport"):
                    found_schemas.append("RegimeReport")
                if hasattr(schemas_module, "EventsReport"):
                    found_schemas.append("EventsReport")
                if found_schemas:
                    break
            except ImportError:
                continue

        if not found_schemas:
            # Check if schemas.py exists as a file
            engine_path = self.project_root / self.engine_paths.get(engine_id, "")
            if (engine_path / "schemas.py").exists():
                return CertificationResult(
                    name="Schemas",
                    status=CertStatus.PARTIAL,
                    score=70.0,
                    details="schemas.py exists but could not be imported",
                    errors=["Schema import failed"],
                )

            return CertificationResult(
                name="Schemas",
                status=CertStatus.PARTIAL,
                score=50.0,
                details="No schema classes found",
                errors=["Missing required schema definitions"],
            )

        return CertificationResult(
            name="Schemas",
            status=CertStatus.CERTIFIED,
            score=100.0,
            details=f"Schemas found: {', '.join(found_schemas)}",
        )

    def _check_asset_impact_matrix(self, engine_id: str) -> CertificationResult:
        """Check if Asset Impact Matrix is correctly implemented"""
        module_path = self.engine_modules.get(engine_id)

        if not module_path:
            return CertificationResult(
                name="Asset Impact Matrix",
                status=CertStatus.FAILED,
                score=0,
                details="Module path not found",
                errors=["Unknown engine"],
            )

        # Try multiple locations
        aim_locations = [
            f"{module_path}.asset_impact_matrix",
            f"{module_path}.impact.asset_impact_matrix",
        ]

        for loc in aim_locations:
            try:
                importlib.import_module(loc)
                return CertificationResult(
                    name="Asset Impact Matrix",
                    status=CertStatus.CERTIFIED,
                    score=100.0,
                    details=f"Asset Impact Matrix found at {loc}",
                )
            except ImportError:
                continue

        # Check if file exists
        engine_path = self.project_root / self.engine_paths.get(engine_id, "")
        if (engine_path / "asset_impact_matrix.py").exists():
            return CertificationResult(
                name="Asset Impact Matrix",
                status=CertStatus.PARTIAL,
                score=70.0,
                details="asset_impact_matrix.py exists but could not be imported",
                errors=["Import failed"],
            )

        if (engine_path / "impact" / "asset_impact_matrix.py").exists():
            return CertificationResult(
                name="Asset Impact Matrix",
                status=CertStatus.PARTIAL,
                score=70.0,
                details="impact/asset_impact_matrix.py exists but could not be imported",
                errors=["Import failed"],
            )

        return CertificationResult(
            name="Asset Impact Matrix",
            status=CertStatus.PARTIAL,
            score=50.0,
            details="Asset Impact Matrix not found",
            errors=["Missing Asset Impact Matrix implementation"],
        )

    def _check_integration(self, engine_id: str) -> CertificationResult:
        """Check integration readiness"""
        module_path = self.engine_modules.get(engine_id)

        if not module_path:
            return CertificationResult(
                name="Integration",
                status=CertStatus.FAILED,
                score=0,
                details="Module path not found",
                errors=["Unknown engine"],
            )

        try:
            constants = importlib.import_module(f"{module_path}.constants")
            if hasattr(constants, "NDIP_TOPICS"):
                ndip_topics = getattr(constants, "NDIP_TOPICS")
                if isinstance(ndip_topics, dict) and len(ndip_topics) > 0:
                    return CertificationResult(
                        name="Integration",
                        status=CertStatus.CERTIFIED,
                        score=100.0,
                        details=f"NDIP topics configured: {len(ndip_topics)} topics",
                    )

            return CertificationResult(
                name="Integration",
                status=CertStatus.PARTIAL,
                score=70.0,
                details="NDIP topics not properly configured",
                errors=["NDIP_TOPICS missing or empty"],
            )

        except ImportError as e:
            if "No module named 'intelligence'" in str(e):
                return CertificationResult(
                    name="Integration",
                    status=CertStatus.BLOCKED,
                    score=0,
                    details="Project import bootstrap failure",
                    errors=[str(e)],
                )
            return CertificationResult(
                name="Integration",
                status=CertStatus.FAILED,
                score=0,
                details=f"Integration check failed: {e}",
                errors=[str(e)],
            )
        except Exception as e:
            return CertificationResult(
                name="Integration",
                status=CertStatus.FAILED,
                score=0,
                details=f"Integration check failed: {e}",
                errors=[str(e)],
            )

    def certify_all(self) -> Dict[str, EngineCertification]:
        """Certify all engines"""
        results = {}

        for engine_id in self.engine_paths.keys():
            results[engine_id] = self.certify_engine(engine_id)

        return results

    def generate_report(self, results: Dict[str, EngineCertification]) -> str:
        """Generate a formatted report"""
        lines = []
        lines.append("\n" + "=" * 70)
        lines.append("NEXUS AI TERMINAL - ENGINE CERTIFICATION REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.utcnow().isoformat()}")
        lines.append("=" * 70)
        lines.append("")

        # Summary table
        lines.append("ENGINE STATUS SUMMARY")
        lines.append("-" * 60)
        lines.append(f"{'Engine':<10} {'Status':<14} {'Score':<8} {'Details'}")
        lines.append("-" * 60)

        for engine_id, cert in sorted(results.items()):
            if cert.status == CertStatus.CERTIFIED:
                status_symbol = "[OK]"
            elif cert.status == CertStatus.PARTIAL:
                status_symbol = "[--]"
            elif cert.status == CertStatus.FAILED:
                status_symbol = "[XX]"
            else:
                status_symbol = "[??]"
            lines.append(
                f"{engine_id:<10} {status_symbol} {cert.status.value:<12} {cert.overall_score:>5.1f}%"
            )

        lines.append("-" * 60)

        # Detailed results
        lines.append("")
        lines.append("DETAILED RESULTS")
        lines.append("=" * 70)

        for engine_id, cert in sorted(results.items()):
            lines.append(f"\n{engine_id} - {cert.status.value}")
            lines.append("-" * 40)
            for result in cert.results:
                if result.status == CertStatus.CERTIFIED:
                    status_symbol = "[OK]"
                elif result.status == CertStatus.PARTIAL:
                    status_symbol = "[--]"
                elif result.status == CertStatus.FAILED:
                    status_symbol = "[XX]"
                else:
                    status_symbol = "[??]"
                lines.append(
                    f"  {status_symbol} {result.name:<25} {result.score:>5.1f}% - {result.details}"
                )

        lines.append("")
        lines.append("=" * 70)

        # Overall stats
        certified = sum(1 for c in results.values() if c.status == CertStatus.CERTIFIED)
        partial = sum(1 for c in results.values() if c.status == CertStatus.PARTIAL)
        failed = sum(1 for c in results.values() if c.status == CertStatus.FAILED)
        blocked = sum(1 for c in results.values() if c.status == CertStatus.BLOCKED)
        total = len(results)
        avg_score = (
            sum(c.overall_score for c in results.values()) / total if total > 0 else 0
        )

        lines.append(
            f"SUMMARY: {certified} CERTIFIED, {partial} PARTIAL, {failed} FAILED, {blocked} BLOCKED"
        )
        lines.append(f"AVERAGE SCORE: {avg_score:.1f}%")
        lines.append("=" * 70)

        return "\n".join(lines)


def main():
    """Main entry point"""
    project_root = str(PROJECT_ROOT)
    certifier = EngineCertifier(project_root)

    print("\n" + "=" * 70)
    print("NEXUS AI TERMINAL - ENGINE CERTIFICATION")
    print("=" * 70)
    print(f"Project Root: {project_root}")
    print(f"Python Path: {sys.path[:3]}")
    print("=" * 70)

    results = certifier.certify_all()
    report = certifier.generate_report(results)
    print(report)

    # Determine exit code
    certified = sum(1 for c in results.values() if c.status == CertStatus.CERTIFIED)
    total = len(results)

    if certified == total:
        print("\n[OK] ALL ENGINES CERTIFIED!")
        sys.exit(0)
    else:
        failed = sum(1 for c in results.values() if c.status == CertStatus.FAILED)
        blocked = sum(1 for c in results.values() if c.status == CertStatus.BLOCKED)
        print(f"\n[WARN] {certified} CERTIFIED, {failed} FAILED, {blocked} BLOCKED")
        sys.exit(1)


if __name__ == "__main__":
    main()
