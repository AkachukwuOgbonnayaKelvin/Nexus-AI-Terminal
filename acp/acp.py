#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACP Architecture OS v4.0
Platform Architecture Compiler for Nexus AI Terminal
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from acp.core.platform_scanner import PlatformScanner
from acp.discovery.engine_discovery import EngineDiscovery
from acp.analyzers.architecture_analyzer import ArchitectureAnalyzer
from acp.analyzers.dependency_analyzer import DependencyAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="ACP Architecture OS v4.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python acp/acp.py scan                    # Scan entire platform
  python acp/acp.py engine TEST-001         # Analyze specific engine (preferred)
  python acp/acp.py engine --engine TEST-001 # Alternative syntax
  python acp/acp.py repair-plan             # Generate repair plan
        """,
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="scan",
        choices=["scan", "engine", "repair-plan", "report"],
        help="Command to execute",
    )

    parser.add_argument("--engine", "-e", type=str, help="Engine ID to analyze")

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )

    parser.add_argument(
        "--json", "-j", action="store_true", help="Output in JSON format"
    )

    # For position-based engine argument: acp.py engine TEST-001
    args, unknown = parser.parse_known_args()

    # Determine project root
    project_root = Path(__file__).parent.parent

    # Handle the case: acp.py engine TEST-001 (engine ID as positional)
    engine_id = args.engine
    if args.command == "engine" and not engine_id and unknown:
        engine_id = unknown[0]

    if args.command == "scan":
        _run_scan(project_root, args.verbose)
    elif args.command == "engine":
        _run_engine_analysis(project_root, engine_id, args.verbose)
    elif args.command == "repair-plan":
        _run_repair_plan(project_root)
    elif args.command == "report":
        _run_report(project_root)
    else:
        _run_scan(project_root, args.verbose)


def _run_scan(project_root: Path, verbose: bool = False):
    """Run platform scan"""
    scanner = PlatformScanner(str(project_root))
    result = scanner.scan()

    print("")
    print("=" * 70)
    print("  ACP ARCHITECTURE OS v4.0 - PLATFORM SCAN")
    print("  Nexus AI Terminal")
    print("=" * 70)

    print("")
    print(f"Project Root: {result['root_path']}")
    print("")
    print("Platform Summary:")
    print(f"  - Registered Engines: {result['summary']['total_engines']}")
    print(f"  - NDIP domains: {result['summary']['ndip_domains']}")
    print(f"  - DAR registrations: {result['summary']['dar_registrations']}")
    print(f"  - Warehouse domains: {result['summary']['warehouse_domains']}")
    print(f"  - Python modules: {result['summary']['total_modules']}")
    print(f"  - Python packages: {result['summary']['total_packages']}")

    if result["engines"]:
        print("")
        print("Discovered Engines:")
        for engine in result["engines"]:
            status = "[OK]" if engine["has_engine_yaml"] else "[MISSING]"
            print(f"  {status} {engine['id']} - {engine['name']}")
            print(f"     Path: {engine['path']}")
            print(f"     Stage: {engine['stage']}")
            if engine["has_engine_yaml"]:
                print(f"     Status: {engine['status']}")

    # Run discovery for unregistered engines
    discovery = EngineDiscovery(str(project_root))
    discovery_result = discovery.discover()

    if discovery_result["probable_engines"]:
        print("")
        print("[WARNING] Probable Unregistered Engines Found:")
        for engine in discovery_result["probable_engines"]:
            print(f"  - {engine['id']} (found at: {engine['path']})")
            print(f"    Reason: {engine['reason']}")
            print(f"    Recommendation: {engine['recommendation']}")

    # Analyze each engine
    print("")
    print("Analyzing Engines:")
    print("-" * 70)
    analyzer = ArchitectureAnalyzer()
    dep_analyzer = DependencyAnalyzer(project_root)

    for engine_dict in result["engines"]:
        engine_path = Path(engine_dict["path"])
        engine_data = engine_dict.get("engine_yaml", {})

        print("")
        print(f"  Engine: {engine_dict['id']}")

        # Architecture analysis
        arch_result = analyzer.analyze(engine_path, engine_data)
        print(f"     Architecture Compliance: {arch_result['compliance_score']}%")
        print(f"     Architecture Maturity: {arch_result['maturity_score']}%")
        print(f"     Overall Health: {arch_result['overall_score']}%")
        print(f"     Status: {arch_result['status']}")

        if arch_result["issues"]:
            for issue in arch_result["issues"]:
                print(f"        [ERROR] {issue['message']}")
                print(f"           Fix: {issue['fix']}")

        if arch_result["info"]:
            for info in arch_result["info"]:
                print(f"        [INFO] {info['message']}")
                if info.get("recommendation"):
                    print(f"           {info['recommendation']}")

        # Dependency analysis
        dep_result = dep_analyzer.analyze(engine_path, engine_data)
        print(f"     Dependencies: {dep_result['score']}% - {dep_result['status']}")

        if dep_result["dependencies"]:
            print(
                f"        Internal Dependencies: {', '.join(dep_result.get('internal_dependencies', []))}"
            )
            print(
                f"        External Dependencies: {', '.join(dep_result.get('external_dependencies', []))}"
            )

    print("")
    print("=" * 70)


def _run_engine_analysis(project_root: Path, engine_id: str, verbose: bool = False):
    """Analyze a specific engine"""
    if not engine_id:
        print("[ERROR] Please specify an engine ID")
        print("Usage: python acp/acp.py engine TEST-001")
        return

    scanner = PlatformScanner(str(project_root))
    result = scanner.scan()

    engine = None
    for e in result["engines"]:
        if e["id"] == engine_id:
            engine = e
            break

    if not engine:
        print(f"[ERROR] Engine '{engine_id}' not found")
        print("Available engines:")
        for e in result["engines"]:
            print(f"  - {e['id']} ({e['name']})")
        return

    print("")
    print("=" * 70)
    print(f"  ENGINE ANALYSIS: {engine['id']}")
    print("=" * 70)

    engine_path = Path(engine["path"])
    engine_data = engine.get("engine_yaml", {})

    analyzer = ArchitectureAnalyzer()
    arch_result = analyzer.analyze(engine_path, engine_data)

    print("")
    print(f"Architecture Compliance: {arch_result['compliance_score']}%")
    print(f"Architecture Maturity: {arch_result['maturity_score']}%")
    print(f"Overall Health: {arch_result['overall_score']}%")
    print(f"Status: {arch_result['status']}")

    print("")
    print("Components:")
    print(
        f"  Required Folders Present: {len(arch_result['present_folders'])}/{len(arch_result['present_folders']) + len(arch_result['missing_folders'])}"
    )
    if arch_result["missing_folders"]:
        print(f"    Missing: {', '.join(arch_result['missing_folders'])}")

    print(
        f"  Required Files Present: {len(arch_result['present_files'])}/{len(arch_result['present_files']) + len(arch_result['missing_files'])}"
    )
    if arch_result["missing_files"]:
        print(f"    Missing: {', '.join(arch_result['missing_files'])}")

    if arch_result["optional_present"]:
        print(
            f"  Optional Components Present: {', '.join(arch_result['optional_present'])}"
        )

    if arch_result["optional_missing"]:
        print(
            f"  Optional Components Missing: {', '.join(arch_result['optional_missing'])}"
        )

    if arch_result["issues"]:
        print("")
        print("Issues:")
        for issue in arch_result["issues"]:
            print(f"  [ERROR] {issue['message']}")
            print(f"    Fix: {issue['fix']}")

    if arch_result["info"]:
        print("")
        print("Information:")
        for info in arch_result["info"]:
            print(f"  [INFO] {info['message']}")
            if info.get("recommendation"):
                print(f"    {info['recommendation']}")

    # Analyze dependencies
    dep_analyzer = DependencyAnalyzer(project_root)
    dep_result = dep_analyzer.analyze(engine_path, engine_data)

    print("")
    print(f"Dependencies: {dep_result['score']}% - {dep_result['status']}")
    if dep_result["dependencies"]:
        print(f"  All Dependencies: {', '.join(dep_result['dependencies'])}")
    if dep_result["internal_dependencies"]:
        print(f"  Internal: {', '.join(dep_result['internal_dependencies'])}")
    if dep_result["external_dependencies"]:
        print(f"  External: {', '.join(dep_result['external_dependencies'])}")

    if dep_result["circular_dependencies"]:
        print("")
        print("Circular Dependencies Detected:")
        for circ in dep_result["circular_dependencies"]:
            print(f"  - {circ}")

    print("")
    print("=" * 70)


def _run_repair_plan(project_root: Path):
    """Generate repair plan"""
    scanner = PlatformScanner(str(project_root))
    result = scanner.scan()

    print("")
    print("=" * 70)
    print("  REPAIR PLAN")
    print("=" * 70)

    repair_items = []

    for engine_dict in result["engines"]:
        engine_path = Path(engine_dict["path"])
        engine_data = engine_dict.get("engine_yaml", {})

        analyzer = ArchitectureAnalyzer()
        arch_result = analyzer.analyze(engine_path, engine_data)

        for issue in arch_result["issues"]:
            repair_items.append(
                {
                    "priority": "Critical",
                    "engine": engine_dict["id"],
                    "type": issue["type"],
                    "message": issue["message"],
                    "fix": issue["fix"],
                }
            )

        for info in arch_result["info"]:
            repair_items.append(
                {
                    "priority": "Info",
                    "engine": engine_dict["id"],
                    "type": info["type"],
                    "message": info["message"],
                    "fix": info.get("recommendation", "Consider implementing"),
                }
            )

    # Also check for unregistered engines
    discovery = EngineDiscovery(str(project_root))
    discovery_result = discovery.discover()

    for engine in discovery_result["probable_engines"]:
        repair_items.append(
            {
                "priority": "High",
                "engine": engine["id"],
                "type": "UNREGISTERED_ENGINE",
                "message": f"Engine found but not registered: {engine['reason']}",
                "fix": engine["recommendation"],
            }
        )

    if repair_items:
        # Sort by priority: Critical > High > Info
        priority_order = {"Critical": 0, "High": 1, "Info": 2}
        repair_items.sort(key=lambda x: priority_order.get(x["priority"], 3))

        print("")
        print(f"Found {len(repair_items)} repair items:")
        for i, item in enumerate(repair_items, 1):
            priority_icon = (
                "[CRITICAL]"
                if item["priority"] == "Critical"
                else "[HIGH]"
                if item["priority"] == "High"
                else "[INFO]"
            )
            print("")
            print(
                f"{i}. {priority_icon} [{item['priority']}] {item['engine']} - {item['type']}"
            )
            print(f"   Issue: {item['message']}")
            print(f"   Fix: {item['fix']}")
    else:
        print("")
        print("[OK] No issues found - platform is healthy!")

    print("")
    print("=" * 70)


def _run_report(project_root: Path):
    """Generate full report"""
    _run_scan(project_root, False)


if __name__ == "__main__":
    main()
