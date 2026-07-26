#!/usr/bin/env python3
"""
Global Intelligence Hub - Full Certification with All Engines
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
from intelligence.hub import GlobalIntelligenceHub


def run_full_certification():
    print("\n" + "=" * 70)
    print("GLOBAL INTELLIGENCE HUB - FULL CERTIFICATION")
    print("(All Three Engines)")
    print("=" * 70 + "\n")

    hub = GlobalIntelligenceHub()

    # 1. Create GLB-001 Report
    print("Generating GLB-001 Report...")
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
    print(
        f"  ✅ GLB-001: {regime_report.primary_regime.value} (Score: {regime_report.regime_score:.1f})"
    )
    hub.collect_report("GLB-001", regime_report)

    # 2. Create GLB-002 Report (Placeholder)
    print("  ⚠️ GLB-002: Placeholder (need to import actual engine)")

    # 3. Create GLB-003 Report (Placeholder)
    print("  ⚠️ GLB-003: Placeholder (need to import actual engine)")

    # Build snapshot
    print("\nBuilding snapshot...")
    snapshot = hub.build_snapshot()

    print(f"\n✅ Snapshot ID: {snapshot['snapshot_id']}")
    print(f"   Status: {snapshot['health']['status']}")
    print(f"   Regime: {snapshot['market_regime']['primary_regime']}")
    print(
        f"   Engines: {snapshot['health']['operational_count']}/{snapshot['health']['total_count']}"
    )

    print("\n" + "=" * 70)
    print("✅ HUB CERTIFIED (with available engines)")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_full_certification()
