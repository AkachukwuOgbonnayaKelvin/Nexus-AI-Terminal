# -*- coding: utf-8 -*-
"""
Console Report - Renders verification results in console
"""

from typing import Dict, Any


class ConsoleReport:
    def __init__(self, results: Dict[str, Any]):
        self.results = results

    def render(self):
        if (
            isinstance(self.results, dict)
            and "engine" in self.results
            and "gates" in self.results
        ):
            self._render_single(self.results)
        elif isinstance(self.results, dict) and "overall_status" in self.results:
            self._render_single(self.results)
        else:
            self._render_multi(self.results)

    def _render_single(self, result: Dict[str, Any]):
        print("\n" + "=" * 70)
        print("  NEXUS ENGINE VERIFICATION REPORT")
        print(f"  Engine: {result.get('engine', 'Unknown')}")
        if result.get("resolved_name"):
            print(f"  Name: {result.get('resolved_name')}")
        print("=" * 70)

        # Show critical failures first
        if result.get("critical_failures"):
            print("\n[CRITICAL FAILURES]")
            for failure in result["critical_failures"]:
                print(f"  ❌ {failure['gate'].upper()}: {failure['reason']}")

        # Show each gate result
        gates = result.get("gates", {})
        if not gates:
            print("\n[ERROR] No gate results found. Check if gates are registered.")
            print("Try running with --verbose flag.")
        else:
            for gate_name, gate_result in gates.items():
                status = gate_result.get("status", "UNKNOWN")

                if status == "PASS":
                    icon = "✅"
                elif status == "FAIL":
                    icon = "❌"
                elif status == "NOT_APPLICABLE":
                    icon = "⊘"
                else:
                    icon = "⚠️"

                print(f"\n[{icon}] {gate_name.upper()}: {status}")
                print(f"   Score: {gate_result.get('score', 0)}%")

                # Show checks
                for check in gate_result.get("checks", []):
                    check_status = check.get("status", "UNKNOWN")
                    if check_status == "PASS":
                        check_icon = "✅"
                    elif check_status == "FAIL":
                        check_icon = "❌"
                    elif check_status == "WARN":
                        check_icon = "⚠️"
                    else:
                        check_icon = "ℹ️"
                    print(
                        f"   {check_icon} {check.get('name', 'Unknown')}: {check.get('message', '')}"
                    )

                # Show issues
                for issue in gate_result.get("issues", []):
                    print(f"   ❌ {issue.get('message', 'Unknown issue')}")
                    if issue.get("fix"):
                        print(f"      Fix: {issue.get('fix')}")

        print("\n" + "=" * 70)
        print(f"  OVERALL STATUS: {result.get('overall_status', 'UNKNOWN')}")
        print("=" * 70 + "\n")

    def _render_multi(self, results: Dict[str, Any]):
        print("\n" + "=" * 70)
        print("  NEXUS ENGINE VERIFICATION REPORT - ALL ENGINES")
        print("=" * 70)

        passed_count = 0
        failed_count = 0

        for engine_id, result in results.items():
            status = result.get("overall_status", "UNKNOWN")

            if status == "PASS":
                icon = "✅"
                passed_count += 1
            elif status == "FAIL":
                icon = "❌"
                failed_count += 1
            elif status == "PARTIAL":
                icon = "⚠️"
                failed_count += 1
            else:
                icon = "❓"

            # Calculate average score
            scores = [
                g.get("score", 0)
                for g in result.get("gates", {}).values()
                if g.get("score", 0) > 0
            ]
            avg_score = int(sum(scores) / len(scores)) if scores else 0

            print(f"\n[{icon}] {engine_id}: {status}")
            print(f"   Average Score: {avg_score}%")

            # Show gate results
            for gate_name, gate_result in result.get("gates", {}).items():
                gate_status = gate_result.get("status", "UNKNOWN")
                if gate_status == "PASS":
                    gate_icon = "✅"
                elif gate_status == "FAIL":
                    gate_icon = "❌"
                elif gate_status == "NOT_APPLICABLE":
                    gate_icon = "⊘"
                else:
                    gate_icon = "⚠️"
                print(
                    f"   {gate_icon} {gate_name.upper()}: {gate_status} ({gate_result.get('score', 0)}%)"
                )

                # Show issues
                for issue in gate_result.get("issues", []):
                    print(f"      ❌ {issue.get('message', '')}")

        print("\n" + "=" * 70)
        print(f"  SUMMARY: {passed_count} PASSED, {failed_count} FAILED")
        print("=" * 70 + "\n")
