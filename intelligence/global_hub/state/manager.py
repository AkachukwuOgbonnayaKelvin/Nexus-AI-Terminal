"""
Global Intelligence Hub - State Manager

Builds and manages the canonical global intelligence state.
"""

import logging
import uuid
from datetime import datetime, timedelta

from ...confluence.contracts import GlobalIntelligenceOutput
from .snapshot import GlobalSnapshot
from .state import GlobalHubState

logger = logging.getLogger(__name__)


class StateManager:
    """
    Builds and manages the canonical Global Hub state.

    The State Manager creates the single source of truth for
    the Global Intelligence Dashboard.
    """

    def __init__(self):
        self._current_state: GlobalHubState | None = None
        self._state_history: dict[str, GlobalHubState] = {}
        self._snapshots: dict[str, GlobalSnapshot] = {}

    def build_state(self, output: GlobalIntelligenceOutput) -> GlobalHubState:
        """
        Build a canonical state from Confluence output.

        Args:
            output: GlobalIntelligenceOutput from Confluence

        Returns:
            GlobalHubState: Canonical state
        """
        state_id = str(uuid.uuid4())[:8]
        generated_at = output.timestamp or datetime.utcnow()
        valid_until = generated_at + timedelta(hours=1)

        # Convert global risks to dict if needed
        global_risks = []
        if output.global_risks:
            for risk in output.global_risks:
                if hasattr(risk, "__dict__"):
                    global_risks.append(risk.__dict__)
                elif isinstance(risk, dict):
                    global_risks.append(risk)

        # Convert global themes to dict if needed
        global_themes = []
        if output.dominant_themes:
            for theme in output.dominant_themes:
                if hasattr(theme, "__dict__"):
                    global_themes.append(theme.__dict__)
                elif isinstance(theme, dict):
                    global_themes.append(theme)

        state = GlobalHubState(
            state_id=state_id,
            generated_at=generated_at,
            valid_until=valid_until,
            global_regime=output.global_regime,
            global_regime_confidence=output.global_regime_confidence,
            global_risk_level=output.global_risk_level,
            global_risk_score=output.global_risk_score,
            global_output=output,
            currency_rankings=output.currency_rankings,
            asset_class_rankings=output.asset_class_rankings,
            entity_rankings=output.entity_rankings,
            global_drivers=output.global_drivers,
            global_risks=global_risks,
            global_themes=global_themes,
            top_opportunities=output.top_opportunities,
            executive_summary=output.executive_summary,
            schema_version="1.0.0",
            ai_executive_summary=None,
            previous_state_id=self._current_state.state_id
            if self._current_state
            else None,
            is_valid=True,
        )

        # Create immutable snapshot
        snapshot_id = str(uuid.uuid4())[:8]
        snapshot = GlobalSnapshot.from_state(state, snapshot_id)

        # Store in history
        self._state_history[state_id] = state
        self._snapshots[state_id] = snapshot
        self._current_state = state

        logger.info(f"State built: {state_id} (regime={state.global_regime})")
        return state

    def get_current_state(self) -> GlobalHubState | None:
        """Get the current canonical state."""
        return self._current_state

    def get_snapshot(self, state_id: str) -> GlobalSnapshot | None:
        """Get an immutable snapshot by state ID."""
        return self._snapshots.get(state_id)

    def get_state(self, state_id: str) -> GlobalHubState | None:
        """Get a specific state by ID."""
        return self._state_history.get(state_id)

    def get_state_history(self, limit: int = 100) -> list[GlobalHubState]:
        """Get recent state history."""
        states = list(self._state_history.values())
        states.sort(key=lambda s: s.generated_at, reverse=True)
        return states[:limit]

    def get_snapshot_history(self, limit: int = 100) -> list[GlobalSnapshot]:
        """Get recent snapshot history."""
        snapshots = list(self._snapshots.values())
        snapshots.sort(key=lambda s: s.generated_at, reverse=True)
        return snapshots[:limit]

    def is_valid(self, state: GlobalHubState) -> bool:
        """Check if a state is still valid."""
        return state.is_valid and datetime.utcnow() <= state.valid_until

    def can_consume(self, state: GlobalHubState, consumer: str = "GUI") -> tuple:
        """
        Check if a state can be consumed by a specific consumer.

        Returns:
            (can_consume, status, message)
        """
        if not self.is_valid(state):
            return (False, "EXPIRED", "State has expired")

        age = state.age_seconds()
        if consumer == "MASTER_ORCHESTRATOR" and age > 1800:  # 30 minutes
            return (False, "STALE", "State is too old for orchestrator consumption")

        if consumer == "GUI" and age > 3600:  # 1 hour
            return (False, "STALE", "State is too old for GUI display")

        return (True, "CURRENT", "State is valid for consumption")

    def invalidate_current(self) -> None:
        """Invalidate the current state."""
        if self._current_state:
            self._current_state.is_valid = False
            logger.info(f"State invalidated: {self._current_state.state_id}")

    def clear_history(self) -> None:
        """Clear state history."""
        self._state_history.clear()
        self._snapshots.clear()
        self._current_state = None
