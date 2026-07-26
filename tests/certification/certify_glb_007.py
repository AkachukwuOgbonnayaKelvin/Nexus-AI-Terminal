#!/usr/bin/env python3
"""
GLB-007 Capital Flows & Liquidity Intelligence Engine Certification
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime

from intelligence.engines.glb_007_capital_flows.constants import (
    NDIP_TOPICS,
)
from intelligence.engines.glb_007_capital_flows.engine import (
    CapitalFlowsEngine,
)


def run_certification():
    print("\n" + "=" * 70)
    print("GLB-007 CAPITAL FLOWS & LIQUIDITY ENGINE CERTIFICATION")
    print("=" * 70 + "\n")

    engine = CapitalFlowsEngine()
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
        test_data = {
            "flows": [
                {
                    "flow_id": "FLOW-001",
                    "asset": "XAUUSD",
                    "region": "GLOBAL",
                    "flow_type": "SAFE_HAVEN",
                    "direction": "INFLOW",
                    "amount": 1250000000,
                    "amount_normalized": 85.0,
                    "velocity": 82.0,
                    "persistence": 74.0,
                    "confidence": 88.0,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "NDIP",
                }
            ]
        }
        engine.consume_ndip(NDIP_TOPICS["CAPITAL_FLOWS"], test_data)
        results.append(("NDIP Consumption", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("NDIP Consumption", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 3: Engine Run
    print("\nTest 3: Engine Run...")
    try:
        liquidity_data = {
            "global_liquidity": 64.5,
            "central_bank_liquidity": 72.0,
            "money_market_liquidity": 61.0,
            "credit_liquidity": 58.0,
            "funding_stress": 32.0,
            "confidence": 82.0,
            "timestamp": datetime.utcnow().isoformat(),
        }
        engine.consume_ndip(NDIP_TOPICS["GLOBAL_LIQUIDITY"], liquidity_data)
        report = engine.run()
        core = report.get("core_intelligence", {})

        # Check core intelligence
        assert core.get("capital_flow_score", 0) > 0
        assert core.get("flow_direction") is not None
        assert core.get("liquidity_score", 0) > 0

        # Check asset impact matrix
        matrix = report.get("asset_impact_matrix")
        assert matrix is not None
        impacts = matrix.get("impacts", {})
        assert len(impacts) > 0

        results.append(("Engine Run", "PASS"))
        print("  ✅ PASS")
        print(f"     Flow Score: {core.get('capital_flow_score', 0):.1f}")
        print(f"     Flow Direction: {core.get('flow_direction', 'UNKNOWN')}")
        print(f"     Liquidity Score: {core.get('liquidity_score', 0):.1f}")
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
        assert health["engine_id"] == "GLB-007"
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
        print("✅ GLB-007 CAPITAL FLOWS & LIQUIDITY ENGINE: CERTIFIED")
    else:
        print("❌ GLB-007 CAPITAL FLOWS & LIQUIDITY ENGINE: NOT CERTIFIED")
        sys.exit(1)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_certification()
