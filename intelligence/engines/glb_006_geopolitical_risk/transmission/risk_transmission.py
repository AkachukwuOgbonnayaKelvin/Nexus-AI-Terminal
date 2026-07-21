"""
GLB-006 Geopolitical Risk Intelligence Engine - Risk Transmission
"""

import logging
from typing import Dict, List

from ..constants import TransmissionChannel, ASSET_EXPOSURE
from ..input.schemas import GeopoliticalEventInput

logger = logging.getLogger(__name__)


class RiskTransmissionEngine:
    """
    Analyze how geopolitical risk transmits through market channels.

    Channels:
    - Risk-Off: Flight to safety
    - Safe-Haven: Safe haven demand
    - Energy Supply: Oil/gas price impact
    - Trade Disruption: Global trade impact
    - Inflation Shock: Inflation pressure
    - Demand Shock: Economic demand impact
    - Supply Shock: Supply chain disruption
    """

    def __init__(self):
        self._asset_exposure = ASSET_EXPOSURE
        self._channel_weights = {
            TransmissionChannel.RISK_OFF: 0.30,
            TransmissionChannel.SAFE_HAVEN: 0.25,
            TransmissionChannel.ENERGY_SUPPLY: 0.15,
            TransmissionChannel.TRADE_DISRUPTION: 0.15,
            TransmissionChannel.INFLATION_SHOCK: 0.10,
            TransmissionChannel.DEMAND_SHOCK: 0.05,
        }

    def analyze_transmission(self, event: GeopoliticalEventInput) -> Dict:
        """
        Analyze risk transmission for a single event.

        Returns:
            Dict with transmission analysis
        """
        channels = self._determine_channels(event)

        return {
            "event_id": event.event_id,
            "channels": channels,
            "primary_channel": self._get_primary_channel(channels),
            "risk_magnitude": self._calculate_magnitude(event, channels),
            "confidence": event.confidence,
        }

    def analyze_global_transmission(self, events: List[GeopoliticalEventInput]) -> Dict:
        """
        Analyze global risk transmission across all events.

        Returns:
            Dict with global transmission analysis
        """
        if not events:
            return {
                "status": "NO_EVENTS",
                "channels": {},
                "primary_channel": "UNKNOWN",
                "risk_magnitude": 0,
                "confidence": 50.0,
            }

        all_channels = {}
        total_magnitude = 0

        for event in events:
            transmission = self.analyze_transmission(event)
            for channel, data in transmission["channels"].items():
                if channel not in all_channels:
                    all_channels[channel] = []
                all_channels[channel].append(data["strength"])
            total_magnitude += transmission["risk_magnitude"]

        # Average channel strengths
        channel_averages = {}
        for channel, strengths in all_channels.items():
            channel_averages[channel] = sum(strengths) / len(strengths)

        # Determine primary channel
        primary_channel = (
            max(channel_averages.items(), key=lambda x: x[1])[0]
            if channel_averages
            else "UNKNOWN"
        )

        return {
            "status": "OPERATIONAL",
            "channels": channel_averages,
            "primary_channel": primary_channel,
            "risk_magnitude": total_magnitude / len(events) if events else 0,
            "channel_count": len(channel_averages),
            "confidence": sum(e.confidence for e in events) / len(events)
            if events
            else 50.0,
        }

    def _determine_channels(self, event: GeopoliticalEventInput) -> Dict:
        """Determine active transmission channels for an event"""
        channels = {}

        # Base channel activation based on event type
        event_type = event.event_type

        if event_type.value in ["MILITARY_CONFLICT", "TERRORISM"]:
            channels[TransmissionChannel.RISK_OFF] = {
                "strength": 0.80,
                "direction": "BEARISH",
            }
            channels[TransmissionChannel.SAFE_HAVEN] = {
                "strength": 0.75,
                "direction": "BULLISH",
            }
            if event.region in ["MIDDLE_EAST", "EAST_ASIA"]:
                channels[TransmissionChannel.ENERGY_SUPPLY] = {
                    "strength": 0.70,
                    "direction": "BULLISH",
                }
                channels[TransmissionChannel.SUPPLY_SHOCK] = {
                    "strength": 0.65,
                    "direction": "BULLISH",
                }

        elif event_type.value == "SANCTIONS":
            channels[TransmissionChannel.TRADE_DISRUPTION] = {
                "strength": 0.70,
                "direction": "BEARISH",
            }
            channels[TransmissionChannel.INFLATION_SHOCK] = {
                "strength": 0.60,
                "direction": "BULLISH",
            }
            if "RU" in event.countries or "IR" in event.countries:
                channels[TransmissionChannel.ENERGY_SUPPLY] = {
                    "strength": 0.55,
                    "direction": "BULLISH",
                }

        elif event_type.value == "TRADE_RESTRICTION":
            channels[TransmissionChannel.TRADE_DISRUPTION] = {
                "strength": 0.75,
                "direction": "BEARISH",
            }
            channels[TransmissionChannel.DEMAND_SHOCK] = {
                "strength": 0.50,
                "direction": "BEARISH",
            }

        elif event_type.value == "ELECTION":
            channels[TransmissionChannel.RISK_OFF] = {
                "strength": 0.40,
                "direction": "BEARISH",
            }

        # Adjust for severity
        severity_factor = event.severity / 100
        for channel in channels:
            channels[channel]["strength"] = min(
                1.0, channels[channel]["strength"] * severity_factor * 1.2
            )

        return channels

    def _get_primary_channel(self, channels: Dict) -> str:
        """Get the primary transmission channel"""
        if not channels:
            return "UNKNOWN"
        return max(channels.items(), key=lambda x: x[1]["strength"])[0].value

    def _calculate_magnitude(
        self, event: GeopoliticalEventInput, channels: Dict
    ) -> float:
        """Calculate risk magnitude"""
        if not channels:
            return 0

        weighted_sum = 0
        total_weight = 0

        for channel, data in channels.items():
            weight = self._channel_weights.get(channel, 0.10)
            weighted_sum += data["strength"] * weight
            total_weight += weight

        return (weighted_sum / total_weight) * 100 if total_weight > 0 else 0
