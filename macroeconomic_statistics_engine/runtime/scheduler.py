# -*- coding: utf-8 -*-
"""MAC-001 Runtime Scheduler - Called by Central Scheduler"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def run_mac001():
    """Run MAC-001 macro data acquisition"""
    print("[MAC-001] Running macro statistics acquisition...")

    try:
        from macroeconomic_statistics_engine.collectors.gdp_collector import (
            GDPCollector,
        )
        from macroeconomic_statistics_engine.collectors.cpi_collector import (
            CPICollector,
        )
        from macroeconomic_statistics_engine.collectors.unemployment_collector import (
            UnemploymentCollector,
        )

        # Run GDP collector
        gdp = GDPCollector()
        gdp_obs = gdp.collect()
        print(f"[MAC-001] GDP: {len(gdp_obs)} observations")

        # Run CPI collector
        cpi = CPICollector()
        cpi_obs = cpi.collect()
        print(f"[MAC-001] CPI: {len(cpi_obs)} observations")

        # Run Unemployment collector
        unemployment = UnemploymentCollector()
        unemployment_obs = unemployment.collect()
        print(f"[MAC-001] Unemployment: {len(unemployment_obs)} observations")

        print("[MAC-001] Macro statistics acquisition complete")
        return {
            "status": "SUCCESS",
            "gdp": len(gdp_obs),
            "cpi": len(cpi_obs),
            "unemployment": len(unemployment_obs),
        }

    except Exception as e:
        print(f"[MAC-001] Error: {e}")
        return {"status": "FAILED", "error": str(e)}


def run_mac001_indicator(indicator: str):
    """Run MAC-001 for a specific indicator"""
    print(f"[MAC-001] Running {indicator} acquisition...")

    try:
        if indicator == "GDP":
            from macroeconomic_statistics_engine.collectors.gdp_collector import (
                GDPCollector,
            )

            collector = GDPCollector()
        elif indicator == "CPI":
            from macroeconomic_statistics_engine.collectors.cpi_collector import (
                CPICollector,
            )

            collector = CPICollector()
        elif indicator == "UNEMPLOYMENT":
            from macroeconomic_statistics_engine.collectors.unemployment_collector import (
                UnemploymentCollector,
            )

            collector = UnemploymentCollector()
        else:
            return {"status": "FAILED", "error": f"Unknown indicator: {indicator}"}

        obs = collector.collect()
        print(f"[MAC-001] {indicator}: {len(obs)} observations")
        return {"status": "SUCCESS", "indicator": indicator, "count": len(obs)}

    except Exception as e:
        print(f"[MAC-001] Error: {e}")
        return {"status": "FAILED", "error": str(e)}
