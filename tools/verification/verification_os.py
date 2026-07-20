#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEXUS ENGINE VERIFICATION OS
Complete engine certification pipeline
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.verification.gates.acp_gate import ACPGate
from tools.verification.gates.eiv_gate import EIVGate
from tools.verification.gates.efl_gate import EFLGate
from tools.verification.gates.lcv_gate import LCVGate
from tools.verification.gates.dqv_gate import DQVGate
from tools.verification.gates.rrt_gate import RRTGate
from tools.verification.gates.e2e_gate import E2EGate
from tools.verification.reports.console_report import ConsoleReport
from tools.verification.resolver import get_resolver


class VerificationOS:
    def __init__(self):
        self.gates = {}
        self.results = {}
        self.resolver = get_resolver()

    def register_gate(self, name: str, gate) -> None:
        """Register a verification gate"""
        self.gates[name] = gate
        print(f"[DEBUG] Registered gate: {name}")

    def verify_engine(
        self, engine_id: str, gates: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Run verification on a specific engine"""
        print(f"[DEBUG] Verifying engine: {engine_id}")

        # Resolve identity first
        identity = self.resolver.resolve(engine_id)
        if not identity:
            print(f"[DEBUG] Engine '{engine_id}' not found by resolver")
            return {
                "engine": engine_id,
                "overall_status": "FAIL",
                "error": f"Engine '{engine_id}' not found",
                "gates": {},
            }

        print(f"[DEBUG] Resolved to: {identity.id} at {identity.path}")

        self.results = {
            "engine": engine_id,
            "resolved_id": identity.id,
            "resolved_name": identity.name,
            "resolved_path": str(identity.path),
            "timestamp": datetime.now().isoformat(),
            "gates": {},
            "overall_status": "PENDING",
            "critical_failures": [],
        }

        # Determine which gates to run
        gates_to_run = gates if gates else list(self.gates.keys())
        print(f"[DEBUG] Gates to run: {gates_to_run}")

        if not gates_to_run:
            print("[DEBUG] No gates to run!")
            return self.results

        for gate_name in gates_to_run:
            if gate_name in self.gates:
                print(f"\n[{gate_name.upper()}] Running {gate_name} gate...")
                try:
                    gate = self.gates[gate_name]
                    result = gate.run(identity.id)
                    self.results["gates"][gate_name] = result

                    print(
                        f"[DEBUG] {gate_name} result: {result.get('status')} (Score: {result.get('score', 0)}%)"
                    )

                    if result.get("status") == "FAIL":
                        self.results["overall_status"] = "FAIL"
                        issues = result.get("issues", [])
                        if issues:
                            self.results["critical_failures"].append(
                                {
                                    "gate": gate_name,
                                    "reason": issues[0].get(
                                        "message", "Unknown failure"
                                    ),
                                }
                            )
                        else:
                            self.results["critical_failures"].append(
                                {
                                    "gate": gate_name,
                                    "reason": "Gate returned FAIL status",
                                }
                            )
                except Exception as e:
                    print(f"Error running {gate_name}: {e}")
                    import traceback

                    traceback.print_exc()
                    self.results["gates"][gate_name] = {
                        "status": "ERROR",
                        "score": 0,
                        "issues": [{"message": str(e)}],
                    }
                    self.results["overall_status"] = "FAIL"
                    self.results["critical_failures"].append(
                        {"gate": gate_name, "reason": str(e)}
                    )
            else:
                print(f"[WARNING] Gate '{gate_name}' not registered")

        # If no critical failures, check partial status
        if self.results["overall_status"] != "FAIL":
            all_passed = all(
                self.results["gates"][g].get("status") in ["PASS", "NOT_APPLICABLE"]
                for g in self.results["gates"]
                if g in self.results["gates"]
            )
            self.results["overall_status"] = "PASS" if all_passed else "PARTIAL"

        return self.results

    def verify_all_engines(self) -> Dict[str, Any]:
        engines = self.resolver.list_all_engines()
        all_results = {}

        for engine_id in engines:
            print(f"\n{'='*60}")
            print(f"VERIFYING: {engine_id}")
            print("=" * 60)
            all_results[engine_id] = self.verify_engine(engine_id)

        return all_results


def main():
    parser = argparse.ArgumentParser(
        description="NEXUS ENGINE VERIFICATION OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--engine", "-e", type=str, help="Engine ID to verify")
    parser.add_argument("--all", "-a", action="store_true", help="Verify all engines")
    parser.add_argument("--gate", "-g", type=str, help="Run a specific gate only")
    parser.add_argument(
        "--gates", "-G", type=str, help="Comma-separated list of gates to run"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )

    args = parser.parse_args()

    vos = VerificationOS()

    # Register all gates
    vos.register_gate("acp", ACPGate())
    vos.register_gate("eiv", EIVGate())
    vos.register_gate("efl", EFLGate())
    vos.register_gate("lcv", LCVGate())
    vos.register_gate("dqv", DQVGate())
    vos.register_gate("rrt", RRTGate())
    vos.register_gate("e2e", E2EGate())

    print(f"[DEBUG] Registered {len(vos.gates)} gates: {list(vos.gates.keys())}")

    gates_to_run = None
    if args.gate:
        gates_to_run = [args.gate]
        print(f"[DEBUG] Running specific gate: {args.gate}")
    elif args.gates:
        gates_to_run = args.gates.split(",")
        print(f"[DEBUG] Running specific gates: {gates_to_run}")

    if args.all:
        results = vos.verify_all_engines()
    elif args.engine:
        results = vos.verify_engine(args.engine, gates_to_run)
    else:
        parser.print_help()
        return

    report = ConsoleReport(results)
    report.render()

    # Exit with appropriate code
    if isinstance(results, dict):
        if results.get("overall_status") in ["FAIL", "PARTIAL"]:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
