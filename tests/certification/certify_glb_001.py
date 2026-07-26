#!/usr/bin/env python3
"""
GLB-001 Market Regime Engine Certification
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime

from intelligence.engines.glb_001_market_regime.constants import (
    NDIP_TOPICS,
)
from intelligence.engines.glb_001_market_regime.engine import (
    MarketRegimeEngine,
)


def run_certification():
    print("\n" + "=" * 70)
    print("GLB-001 MARKET REGIME ENGINE CERTIFICATION")
    print("=" * 70 + "\n")

    engine = MarketRegimeEngine()
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
        test_payload = {
            "symbols": {"US500": {"close": 5200, "change_20d": 0.05}},
            "timestamp": datetime.utcnow().isoformat(),
        }
        engine.consume_ndip(NDIP_TOPICS["PRICE_SNAPSHOT"], test_payload)
        results.append(("NDIP Consumption", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("NDIP Consumption", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 3: Engine Run
    print("\nTest 3: Engine Run...")
    try:
        for topic in [
            NDIP_TOPICS["TREND_SNAPSHOT"],
            NDIP_TOPICS["VOLATILITY_SNAPSHOT"],
        ]:
            engine.consume_ndip(topic, {"value": 50})

        report = engine.run()

        assert report.regime_score >= 0
        assert report.regime_score <= 100
        assert report.confidence >= 0
        assert report.confidence <= 100
        assert report.primary_regime is not None
        assert len(report.evidence) > 0

        results.append(("Engine Run", "PASS"))
        print("  ✅ PASS")
        print(f"     Regime: {report.primary_regime.value}")
        print(f"     Score: {report.regime_score:.1f}")
        print(f"     Confidence: {report.confidence:.1f}%")
    except Exception as e:
        results.append(("Engine Run", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 4: Report Generation
    print("\nTest 4: Report Generation...")
    try:
        report = engine.get_last_report()
        assert report is not None
        assert hasattr(report, "asset_context")
        assert len(report.asset_context) > 0
        results.append(("Report Generation", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("Report Generation", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 5: Health Check
    print("\nTest 5: Health Check...")
    try:
        health = engine.health_check()
        assert health["engine_id"] == "GLB-001"
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
        print("✅ GLB-001 MARKET REGIME ENGINE: CERTIFIED")
    else:
        print("❌ GLB-001 MARKET REGIME ENGINE: NOT CERTIFIED")
        sys.exit(1)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_certification()
