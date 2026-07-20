# -*- coding: utf-8 -*-
"""Dataset State Registry - Tracks state of each dataset"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class UpdatePolicy(Enum):
    CONTINUOUS = "continuous"       # MKT-001 - 24/7 live data
    RELEASE_AWARE = "release_aware"  # MAC-001, COT-001 - Official releases
    EVENT_DRIVEN = "event_driven"   # ECO-002, CENT-001 - Events


class DatasetStatus(Enum):
    WAITING = "waiting"
    DUE = "due"
    ACQUIRING = "acquiring"
    VALIDATING = "validating"
    DEDUPLICATING = "deduplicating"
    WAREHOUSE_COMMITTED = "warehouse_committed"
    NDIP_PUBLISHED = "ndip_published"
    COMPLETE = "complete"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class DatasetState:
    """State of a single dataset"""
    dataset_id: str
    engine_id: str
    update_policy: UpdatePolicy
    historical_loaded: bool = False
    last_observation_period: Optional[str] = None
    last_successful_fetch: Optional[datetime] = None
    last_release_id: Optional[str] = None
    next_expected_release: Optional[str] = None
    status: DatasetStatus = DatasetStatus.WAITING
    run_count: int = 0
    last_error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class DatasetStateRegistry:
    """Registry for all dataset states"""
    
    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or Path("orchestrator/state/dataset_states.json")
        self.states: Dict[str, DatasetState] = {}
        self._load()
    
    def _load(self):
        """Load states from file"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    data = json.load(f)
                for key, value in data.items():
                    self.states[key] = DatasetState(
                        dataset_id=value["dataset_id"],
                        engine_id=value["engine_id"],
                        update_policy=UpdatePolicy(value["update_policy"]),
                        historical_loaded=value.get("historical_loaded", False),
                        last_observation_period=value.get("last_observation_period"),
                        last_successful_fetch=datetime.fromisoformat(value["last_successful_fetch"]) if value.get("last_successful_fetch") else None,
                        last_release_id=value.get("last_release_id"),
                        next_expected_release=value.get("next_expected_release"),
                        status=DatasetStatus(value.get("status", "waiting")),
                        run_count=value.get("run_count", 0),
                        last_error=value.get("last_error"),
                        metadata=value.get("metadata", {})
                    )
            except Exception as e:
                print(f"Error loading state: {e}")
    
    def save(self):
        """Save states to file"""
        data = {}
        for key, state in self.states.items():
            data[key] = {
                "dataset_id": state.dataset_id,
                "engine_id": state.engine_id,
                "update_policy": state.update_policy.value,
                "historical_loaded": state.historical_loaded,
                "last_observation_period": state.last_observation_period,
                "last_successful_fetch": state.last_successful_fetch.isoformat() if state.last_successful_fetch else None,
                "last_release_id": state.last_release_id,
                "next_expected_release": state.next_expected_release,
                "status": state.status.value,
                "run_count": state.run_count,
                "last_error": state.last_error,
                "metadata": state.metadata
            }
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get(self, dataset_id: str) -> Optional[DatasetState]:
        return self.states.get(dataset_id)
    
    def register(self, state: DatasetState):
        self.states[state.dataset_id] = state
        self.save()
    
    def update_status(self, dataset_id: str, status: DatasetStatus):
        if dataset_id in self.states:
            self.states[dataset_id].status = status
            self.save()
    
    def get_due_datasets(self) -> list:
        """Get datasets that are due for execution"""
        due = []
        for state in self.states.values():
            if state.status in [DatasetStatus.WAITING, DatasetStatus.DUE]:
                due.append(state)
        return due
    
    def get_by_engine(self, engine_id: str) -> list:
        return [s for s in self.states.values() if s.engine_id == engine_id]
