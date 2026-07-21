# -*- coding: utf-8 -*-
"""Engine Registry - Registers all engines with the scheduler"""

from orchestrator.scheduler.core import CentralScheduler


def register_all_engines(scheduler: CentralScheduler):
    """Register all raw data engines with the scheduler"""

    # MKT-001 - Continuous (24/7 market data)
    scheduler.register_dataset(
        dataset_id="MKT-001_MARKET_PRICES",
        engine_id="MKT-001",
        update_policy="continuous",
        interval_minutes=1,
    )

    # MAC-001 - Release-aware (CPI, GDP, Employment)
    # CPI - Monthly
    scheduler.register_dataset(
        dataset_id="MAC-001_US_CPI",
        engine_id="MAC-001",
        update_policy="release_aware",
        frequency="monthly",
        day_of_month=15,
        time_of_day="08:30",
    )

    # GDP - Quarterly
    scheduler.register_dataset(
        dataset_id="MAC-001_US_GDP",
        engine_id="MAC-001",
        update_policy="release_aware",
        frequency="quarterly",
        day_of_month=25,
        time_of_day="08:30",
    )

    # Employment - Monthly
    scheduler.register_dataset(
        dataset_id="MAC-001_US_EMPLOYMENT",
        engine_id="MAC-001",
        update_policy="release_aware",
        frequency="monthly",
        day_of_month=3,
        time_of_day="08:30",
    )

    # ECO-002 - Event-driven (Earnings releases)
    scheduler.register_dataset(
        dataset_id="ECO-002_EARNINGS", engine_id="ECO-002", update_policy="event_driven"
    )

    # CENT-001 - Event-driven (Central bank announcements)
    scheduler.register_dataset(
        dataset_id="CENT-001_ANNOUNCEMENTS",
        engine_id="CENT-001",
        update_policy="event_driven",
    )

    # INS-001 - Release-aware (COT - Weekly Friday)
    scheduler.register_dataset(
        dataset_id="INS-001_COT",
        engine_id="INS-001",
        update_policy="release_aware",
        frequency="weekly",
        day_of_week=4,  # Friday
        time_of_day="15:30",
    )

    print("✅ All engines registered with scheduler")
