# -*- coding: utf-8 -*-
"""Raw Backend Certification Runner"""

import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.verification.raw_backend_certification.auditors.mkt001_auditor import (
    MKT001Auditor,
)
from tools.verification.raw_backend_certification.auditors.mac001_auditor import (
    MAC001Auditor,
)
from tools.verification.raw_backend_certification.auditors.eco002_auditor import (
    ECO002Auditor,
)
from tools.verification.raw_backend_certification.reports.report_generator import (
    ReportGenerator,
)


class CertificationRunner:
    """Runs raw backend certification for all engines"""

    def __init__(self):
        self.engines = {
            "MKT-001": MKT001Auditor(),
            "MAC-001": MAC001Auditor(),
            "ECO-002": ECO002Auditor(),
        }
        self.results: Dict[str, Any] = {}

    def run_all(self) -> Dict[str, Any]:
        """Run certification for all engines"""
        print("\n" + "=" * 70)
        print("  NEXUS RAW DATA BACKEND CERTIFICATION")
        print("=" * 70)
        print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print("")

        for engine_id, auditor in self.engines.items():
            print(f"[{engine_id}] Running certification...")
            try:
                result = auditor.run_all()
                self.results[engine_id] = result

                status_icon = (
                    "✅"
                    if result.status == "CERTIFIED"
                    else "⚠️"
                    if result.status == "PARTIAL"
                    else "❌"
                )
                print(f"  {status_icon} {result.engine_name}: {result.status}")
                print("")
            except Exception as e:
                print(f"  ❌ Error running {engine_id}: {e}")
                print("")

        # Generate final report
        report = ReportGenerator(self.results)
        report.print_summary()

        return self.results

    def get_certification_status(self) -> str:
        """Get overall certification status"""
        if not self.results:
            return "NOT_RUN"

        statuses = [r.status for r in self.results.values()]
        if all(s == "CERTIFIED" for s in statuses):
            return "CERTIFIED"
        elif any(s == "FAILED" for s in statuses):
            return "FAILED"
        else:
            return "PARTIAL"


def main():
    """Main entry point"""
    runner = CertificationRunner()
    results = runner.run_all()

    # Exit with appropriate code
    status = runner.get_certification_status()
    if status == "CERTIFIED":
        print("\n✅ RAW BACKEND: CERTIFIED")
        print("✅ Consumer engines can now begin.")
        sys.exit(0)
    elif status == "PARTIAL":
        print("\n⚠️ RAW BACKEND: PARTIAL")
        print("⚠️ Some issues found. Review the report above.")
        sys.exit(1)
    else:
        print("\n❌ RAW BACKEND: NOT CERTIFIED")
        print("❌ Fix the issues above before building consumer engines.")
        sys.exit(2)


if __name__ == "__main__":
    main()
