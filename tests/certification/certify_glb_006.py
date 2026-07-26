#!/usr/bin/env python3
"""
GLB-006 Geopolitical Risk Intelligence Engine Certification
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime

from intelligence.engines.glb_006_geopolitical_risk.constants import (
    NDIP_TOPICS,
)
from intelligence.engines.glb_006_geopolitical_risk.engine import (
    GeopoliticalRiskEngine,
)


def run_certification():
    print("\n" + "=" * 70)
    print("GLB-006 GEOPOLITICAL RISK INTELLIGENCE ENGINE CERTIFICATION")
    print("=" * 70 + "\n")

    engine = GeopoliticalRiskEngine()
    passed = True
    results = []

    # Test 1: Engine Initialization
    print("Test 1: Engine Initialization...")
    try:
        assert engine is not None
        results.append(("Engine Initialization", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("Engine Initialization", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 2: NDIP Consumption
    print("\nTest 2: NDIP Consumption...")
    try:
        test_events = {
            "events": [
                {
                    "event_id": "GEO-001",
                    "event_type": "MILITARY_CONFLICT",
                    "headline": "Military escalation in Middle East",
                    "countries": ["SA", "IR"],
                    "region": "MIDDLE_EAST",
                    "severity": 85.0,
                    "escalation_probability": 80.0,
                    "strategic_importance": 90.0,
                    "economic_exposure": 85.0,
                    "market_sensitivity": 90.0,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "INTEL",
                    "confidence": 88.0,
                }
            ]
        }
        engine.consume_ndip(NDIP_TOPICS["GEOPOLITICAL_EVENTS"], test_events)
        results.append(("NDIP Consumption", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("NDIP Consumption", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 3: Engine Run
    print("\nTest 3: Engine Run...")
    try:
        report = engine.run()
        core = report.get("core_intelligence", {})

        # Check core intelligence
        assert core.get("global_geopolitical_risk", 0) > 0
        assert core.get("risk_state") in [
            "CRITICAL",
            "HIGH",
            "ELEVATED",
            "MODERATE",
            "LOW",
        ]
        assert core.get("dominant_theme") is not None
        assert core.get("confidence", 0) > 0

        # Check asset impact matrix
        matrix = report.get("asset_impact_matrix")
        assert matrix is not None
        impacts = matrix.get("impacts", {})
        assert len(impacts) > 0

        results.append(("Engine Run", "PASS"))
        print("  ✅ PASS")
        print(f"     Risk Score: {core.get('global_geopolitical_risk', 0):.1f}")
        print(f"     Risk State: {core.get('risk_state', 'UNKNOWN')}")
        print(f"     Assets: {len(impacts)}")
    except Exception as e:
        results.append(("Engine Run", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 4: Asset Impact Matrix Validation
    print("\nTest 4: Asset Impact Matrix Validation...")
    try:
        report = engine.get_last_report()
        matrix = report.get("asset_impact_matrix")
        impacts = matrix.get("impacts", {})

        # Check score range for all assets
        for asset, impact in impacts.items():
            score = impact.get("score", 0)
            assert -100 <= score <= 100, f"Score {score} out of range for {asset}"

        # Check direction is valid
        for asset, impact in impacts.items():
            direction = impact.get("direction", "NEUTRAL")
            assert direction in [
                "BULLISH",
                "BEARISH",
                "NEUTRAL",
            ], f"Invalid direction {direction} for {asset}"

        results.append(("Asset Impact Matrix Validation", "PASS"))
        print("  ✅ PASS")
        print(f"     All {len(impacts)} assets validated")
    except Exception as e:
        results.append(("Asset Impact Matrix Validation", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 5: Health Check
    print("\nTest 5: Health Check...")
    try:
        health = engine.health_check()
        assert health["engine_id"] == "GLB-006"
        assert health["status"] == "OPERATIONAL"
        results.append(("Health Check", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("Health Check", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("CERTIFICATION SUMMARY")
    print("=" * 70)

    for test, result in results:
        status = "✅" if "PASS" in result else "❌"
        print(f"{status} {test}: {result}")

    print("\n" + "=" * 70)
    if passed:
        print("✅ GLB-006 GEOPOLITICAL RISK INTELLIGENCE ENGINE: CERTIFIED")
    else:
        print("❌ GLB-006 GEOPOLITICAL RISK INTELLIGENCE ENGINE: NOT CERTIFIED")
        sys.exit(1)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_certification()
