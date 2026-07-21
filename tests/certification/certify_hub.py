#!/usr/bin/env python3
"""
Global Intelligence Hub Certification
"""

import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datetime import datetime  # noqa: E402
from intelligence.hub import GlobalIntelligenceHub  # noqa: E402
from intelligence.engines.glb_001_market_regime.engine import MarketRegimeEngine  # noqa: E402
from intelligence.engines.glb_001_market_regime.constants import NDIP_TOPICS  # noqa: E402


def run_certification():
    print("\n" + "=" * 70)
    print("GLOBAL INTELLIGENCE HUB CERTIFICATION")
    print("=" * 70 + "\n")

    passed = True
    results = []

    # Test 1: Hub Initialization
    print("Test 1: Hub Initialization...")
    try:
        hub = GlobalIntelligenceHub()
        assert hub is not None
        results.append(("Hub Initialization", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("Hub Initialization", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 2: Collect Reports
    print("\nTest 2: Collect Reports...")
    try:
        # Create test reports
        regime_engine = MarketRegimeEngine()
        regime_engine.consume_ndip(
            NDIP_TOPICS["PRICE_SNAPSHOT"],
            {
                "symbols": {"US500": {"close": 5200, "change_20d": 0.05}},
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
        regime_engine.consume_ndip(
            NDIP_TOPICS["TREND_SNAPSHOT"], {"direction": "BULLISH", "strength": 75}
        )
        regime_engine.consume_ndip(NDIP_TOPICS["VOLATILITY_SNAPSHOT"], {"vix": 14.2})
        regime_engine.consume_ndip(
            NDIP_TOPICS["MACRO_CONDITIONS"],
            {
                "growth": {"score": 72},
                "inflation": {"score": 35},
                "employment": {"score": 68},
            },
        )
        regime_report = regime_engine.run()

        hub.collect_report("GLB-001", regime_report)
        results.append(("Collect Reports", "PASS"))
        print("  ✅ PASS")
    except Exception as e:
        results.append(("Collect Reports", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 3: Build Snapshot
    print("\nTest 3: Build Snapshot...")
    try:
        snapshot = hub.build_snapshot()
        assert snapshot is not None
        assert "snapshot_id" in snapshot
        assert "market_regime" in snapshot
        results.append(("Build Snapshot", "PASS"))
        print("  ✅ PASS")
        print(f"     Snapshot ID: {snapshot['snapshot_id']}")
        print(f"     Status: {snapshot['health']['status']}")
    except Exception as e:
        results.append(("Build Snapshot", f"FAIL: {e}"))
        passed = False
        print(f"  ❌ FAIL: {e}")

    # Test 4: Health Check
    print("\nTest 4: Health Check...")
    try:
        health = hub.health_check()
        assert health["hub_id"] == "GLOBAL_INTELLIGENCE_HUB"
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
        print("✅ GLOBAL INTELLIGENCE HUB: CERTIFIED")
    else:
        print("❌ GLOBAL INTELLIGENCE HUB: NOT CERTIFIED")
        sys.exit(1)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_certification()
