"""
TOSP Hub – updated with hysteresis, promotion/demotion, and event publishing.
"""

import logging
from dataclasses import dataclass
from datetime import datetime

from ..enums import EventPriority, ProfileEventType
from ..models import Candidate, MarketProfileResult, ProfileEvent

logger = logging.getLogger(__name__)


@dataclass
class TOSPState:
    """State of a candidate in TOSP."""

    symbol: str
    score: float
    entry_time: datetime
    last_update: datetime
    stale_count: int = 0
    eligible: bool = True


class TOSPHub:
    """
    TOSP Hub with hysteresis, promotion/demotion, and event publishing.
    """

    def __init__(
        self,
        redis_client=None,
        db_connection=None,
        cache_key_prefix: str = "tosp:",
        table_name: str = "tosp_candidates",
        promotion_threshold: float = 80.0,
        demotion_threshold: float = 72.0,
        max_stale_hours: float = 48.0,
        event_callback=None,
    ):
        self.redis = redis_client
        self.db = db_connection
        self.cache_key_prefix = cache_key_prefix
        self.table_name = table_name
        self.promotion_threshold = promotion_threshold
        self.demotion_threshold = demotion_threshold
        self.max_stale_hours = max_stale_hours

        self._current_state: dict[str, TOSPState] = {}
        self._history: list[MarketProfileResult] = []
        self._event_callback = event_callback

    def save_candidates(
        self, new_result: MarketProfileResult
    ) -> tuple[str, list[ProfileEvent]]:
        """
        Save candidates with hysteresis. Returns action and list of events.
        """
        events = []
        new_scores = {c.symbol: c.opportunity_score for c in new_result.candidates}
        new_candidates = {c.symbol: c for c in new_result.candidates}

        # 1. Update existing states
        for symbol, state in list(self._current_state.items()):
            if symbol in new_scores:
                score = new_scores[symbol]
                # Check if it's still above demotion threshold
                if score < self.demotion_threshold:
                    # Demote
                    state.eligible = False
                    state.last_update = datetime.now()
                    events.append(
                        ProfileEvent(
                            event_type=ProfileEventType.TOSP_EXIT,
                            symbol=symbol,
                            timestamp=datetime.now(),
                            priority=EventPriority.MEDIUM,
                            reason=f"Score {score:.1f} below demotion threshold {self.demotion_threshold}",
                        )
                    )
                else:
                    # Update
                    state.score = score
                    state.last_update = datetime.now()
            else:
                # Symbol no longer in candidates
                state.eligible = False
                state.last_update = datetime.now()
                events.append(
                    ProfileEvent(
                        event_type=ProfileEventType.TOSP_EXIT,
                        symbol=symbol,
                        timestamp=datetime.now(),
                        priority=EventPriority.LOW,
                        reason="Removed from candidate list",
                    )
                )

        # 2. Promote new candidates
        for symbol, cand in new_candidates.items():
            if symbol not in self._current_state:
                if cand.opportunity_score >= self.promotion_threshold:
                    self._current_state[symbol] = TOSPState(
                        symbol=symbol,
                        score=cand.opportunity_score,
                        entry_time=datetime.now(),
                        last_update=datetime.now(),
                        eligible=True,
                    )
                    events.append(
                        ProfileEvent(
                            event_type=ProfileEventType.TOSP_ENTRY,
                            symbol=symbol,
                            timestamp=datetime.now(),
                            priority=EventPriority.HIGH,
                            reason=f"Score {cand.opportunity_score:.1f} >= promotion threshold {self.promotion_threshold}",
                        )
                    )
                else:
                    # Still a candidate but not yet promoted
                    pass
            else:
                # Already in state, update if eligible
                if self._current_state[symbol].eligible:
                    self._current_state[symbol].score = cand.opportunity_score
                    self._current_state[symbol].last_update = datetime.now()

        # 3. Remove stale entries
        now = datetime.now()
        for symbol, state in list(self._current_state.items()):
            if state.eligible and state.last_update:
                age_hours = (now - state.last_update).total_seconds() / 3600.0
                if age_hours > self.max_stale_hours:
                    state.eligible = False
                    events.append(
                        ProfileEvent(
                            event_type=ProfileEventType.TOSP_EXIT,
                            symbol=symbol,
                            timestamp=now,
                            priority=EventPriority.LOW,
                            reason=f"Stale: {age_hours:.1f}h > {self.max_stale_hours}h",
                        )
                    )

        # 4. Build final candidate list from eligible states
        final_candidates = []
        for symbol, state in self._current_state.items():
            if state.eligible:
                cand = new_candidates.get(symbol)
                if cand:
                    final_candidates.append(cand)

        # 5. Update result with filtered candidates
        new_result.candidates = final_candidates

        # 6. Persist and publish events
        self._persist_current_state()
        if self._event_callback:
            for event in events:
                self._event_callback(event)

        return "updated", events

    def _persist_current_state(self):
        # Same as before, but persist the eligible candidates
        pass

    def get_latest_candidate_symbols(self) -> list[str]:
        """Return symbols of eligible candidates."""
        return [s for s, st in self._current_state.items() if st.eligible]

    def get_latest_candidates(self) -> list[Candidate]:
        # Implement retrieval from cache/DB
        pass

    # ... other methods as before
