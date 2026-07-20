import logging
from statistics import mean, stdev
from typing import List, Optional

from macroeconomic_events_engine.dtos import UniversalMacroEvent

logger = logging.getLogger(__name__)


class ConsensusResolver:
    def resolve(
        self, events: List[UniversalMacroEvent]
    ) -> Optional[UniversalMacroEvent]:
        if not events:
            return None
        # Group by event ID (assuming same event from different providers)
        grouped = {}
        for ev in events:
            key = ev.event_id.split("_")[0] if "_" in ev.event_id else ev.event_id
            grouped.setdefault(key, []).append(ev)

        consensus_events = []
        for key, evs in grouped.items():
            if len(evs) == 1:
                consensus_events.append(evs[0])
                continue
            # Aggregate forecasts
            forecasts = [e.forecast for e in evs if e.forecast is not None]
            consensus_forecast = None
            confidence = 1.0
            if forecasts:
                consensus_forecast = mean(forecasts)
                if len(forecasts) > 1:
                    std = stdev(forecasts)
                    confidence = 1.0 - (std / (abs(consensus_forecast) + 0.001))
                    confidence = max(0.0, min(1.0, confidence))
            # Take the most complete event as base
            base = evs[0]
            base.consensus = consensus_forecast
            base.confidence = confidence
            # Use previous from the most reliable provider (e.g., TradingEconomics)
            for e in evs:
                if e.previous is not None:
                    base.previous = e.previous
                    break
            for e in evs:
                if e.actual is not None:
                    base.actual = e.actual
                    break
            consensus_events.append(base)

        return consensus_events[0] if consensus_events else None
