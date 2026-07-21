# -*- coding: utf-8 -*-
"""Central Scheduler - Owns all execution timing"""

from typing import Dict
from datetime import datetime
import logging
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from orchestrator.state.dataset_state import (
    DatasetStateRegistry,
    DatasetState,
    DatasetStatus,
    UpdatePolicy,
)
from orchestrator.release_calendar.calendar import ReleaseCalendar, ReleaseSchedule
from orchestrator.policies.continuous import ContinuousPolicy
from orchestrator.policies.release_aware import ReleaseAwarePolicy
from orchestrator.policies.event_driven import EventDrivenPolicy


logger = logging.getLogger(__name__)


class CentralScheduler:
    """Central Scheduler - Owns all execution timing"""

    def __init__(self):
        self.registry = DatasetStateRegistry()
        self.calendar = ReleaseCalendar()
        self.policies: Dict[str, any] = {}
        self.running = False
        self.cycle_id = 0

    def register_dataset(
        self,
        dataset_id: str,
        engine_id: str,
        update_policy: str,
        frequency: str = None,
        day_of_week: int = None,
        day_of_month: int = None,
        time_of_day: str = "00:00",
        interval_minutes: int = 1,
    ):
        """Register a dataset with the scheduler"""

        # Create dataset state
        state = DatasetState(
            dataset_id=dataset_id,
            engine_id=engine_id,
            update_policy=UpdatePolicy(update_policy),
        )
        self.registry.register(state)

        # Create policy based on update type
        if update_policy == "continuous":
            policy = ContinuousPolicy(interval_minutes=interval_minutes)
            self.policies[dataset_id] = policy

        elif update_policy == "release_aware":
            # Register release schedule
            schedule = ReleaseSchedule(
                dataset_id=dataset_id,
                frequency=frequency,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                time_of_day=time_of_day,
            )
            self.calendar.register(schedule)

            policy = ReleaseAwarePolicy(self.calendar)
            self.policies[dataset_id] = policy

        elif update_policy == "event_driven":
            policy = EventDrivenPolicy()
            self.policies[dataset_id] = policy

        logger.info(
            f"Registered dataset: {dataset_id} (engine: {engine_id}, policy: {update_policy})"
        )

        return state

    def check_and_run(self):
        """Check all datasets and run due ones"""
        self.cycle_id += 1
        cycle_id = (
            f"CYCLE-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{self.cycle_id:04d}"
        )

        logger.info(f"=== Starting cycle: {cycle_id} ===")

        results = {
            "cycle_id": cycle_id,
            "timestamp": datetime.now().isoformat(),
            "runs": [],
        }

        for dataset_id, policy in self.policies.items():
            try:
                if policy.is_due(dataset_id):
                    state = self.registry.get(dataset_id)
                    if state:
                        logger.info(f"  Dataset {dataset_id} is DUE")
                        result = self._run_dataset(dataset_id, cycle_id)
                        results["runs"].append(result)
                    else:
                        logger.warning(f"  Dataset {dataset_id} has no state")
                else:
                    logger.debug(f"  Dataset {dataset_id} not due")
            except Exception as e:
                logger.error(f"Error checking {dataset_id}: {e}")

        logger.info(f"=== Cycle {cycle_id} complete ===")

        return results

    def _run_dataset(self, dataset_id: str, cycle_id: str) -> Dict:
        """Run a single dataset by calling the actual engine"""
        state = self.registry.get(dataset_id)
        if not state:
            return {"dataset_id": dataset_id, "status": "ERROR", "message": "No state"}

        logger.info(f"    Running {dataset_id}...")
        state.status = DatasetStatus.ACQUIRING
        state.run_count += 1
        self.registry.save()

        result = {"dataset_id": dataset_id, "status": "PENDING"}

        try:
            # Call the appropriate engine based on dataset_id
            if dataset_id.startswith("MKT-001"):
                from market_price_engine.runtime.scheduler import run_mkt001

                engine_result = run_mkt001()
                result["engine_result"] = engine_result

            elif dataset_id.startswith("MAC-001"):
                from macroeconomic_statistics_engine.runtime.scheduler import run_mac001

                engine_result = run_mac001()
                result["engine_result"] = engine_result

            elif dataset_id.startswith("ECO-002"):
                from corporate_earnings_engine.runtime.scheduler import run_eco002

                engine_result = run_eco002()
                result["engine_result"] = engine_result

            elif dataset_id.startswith("CENT-001"):
                # Central Bank Engine - to be implemented
                result["engine_result"] = {
                    "status": "SKIPPED",
                    "message": "Not yet implemented",
                }

            elif dataset_id.startswith("INS-001"):
                # Institutional Positioning Engine - to be implemented
                result["engine_result"] = {
                    "status": "SKIPPED",
                    "message": "Not yet implemented",
                }

            else:
                result["engine_result"] = {
                    "status": "UNKNOWN",
                    "message": f"Unknown dataset: {dataset_id}",
                }

            # Check if engine execution was successful
            if result["engine_result"].get("status") == "SUCCESS":
                state.status = DatasetStatus.COMPLETE
                state.last_successful_fetch = datetime.now()
                result["status"] = "COMPLETE"
            else:
                state.status = DatasetStatus.FAILED
                state.last_error = result["engine_result"].get("error", "Unknown error")
                result["status"] = "FAILED"

            self.registry.save()
            logger.info(f"    {dataset_id}: {result['status']}")

        except Exception as e:
            state.status = DatasetStatus.FAILED
            state.last_error = str(e)
            self.registry.save()
            result["status"] = "FAILED"
            result["error"] = str(e)
            logger.error(f"    {dataset_id} FAILED: {e}")

        return result

    def run_once(self):
        """Run one scheduler cycle"""
        return self.check_and_run()

    def run_forever(self):
        """Run the scheduler continuously"""
        self.running = True
        while self.running:
            self.check_and_run()
            time.sleep(60)  # Check every minute

    def stop(self):
        self.running = False
