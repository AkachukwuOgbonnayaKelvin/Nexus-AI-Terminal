"""
GLB-007 Capital Flows & Liquidity Intelligence Engine - Flow Analyzer
"""

import logging
from collections import defaultdict
from typing import Any

from ..constants import FlowDirection, FlowMomentum
from ..input.schemas import CapitalFlowInput

logger = logging.getLogger(__name__)


class FlowAnalyzer:
    """Analyze capital flows"""

    def analyze_flows(self, flows: list[CapitalFlowInput]) -> dict[str, Any]:
        """
        Analyze capital flows and produce flow intelligence.

        Returns:
            Dict with flow analysis
        """
        if not flows:
            return {
                "status": "NO_FLOWS",
                "flow_count": 0,
                "dominant_flow": "UNKNOWN",
                "flow_direction": "NEUTRAL",
                "flow_strength": 0,
                "confidence": 0,
            }

        # Calculate aggregate flow metrics
        total_inflow = sum(
            f.amount_normalized for f in flows if f.direction == FlowDirection.INFLOW
        )
        total_outflow = sum(
            f.amount_normalized for f in flows if f.direction == FlowDirection.OUTFLOW
        )
        total_flows = len(flows)

        # Calculate net flow
        net_flow = total_inflow - total_outflow

        # Determine dominant flow type
        flow_types = defaultdict(float)
        for flow in flows:
            flow_types[flow.flow_type.value] += (
                flow.amount_normalized * flow.confidence / 100
            )

        dominant_flow = (
            max(flow_types.items(), key=lambda x: x[1])[0] if flow_types else "UNKNOWN"
        )

        # Determine flow direction
        if net_flow > 20:
            direction = "INFLOW"
        elif net_flow < -20:
            direction = "OUTFLOW"
        else:
            direction = "NEUTRAL"

        # Calculate flow strength
        avg_amount = (
            sum(f.amount_normalized for f in flows) / total_flows
            if total_flows > 0
            else 0
        )
        avg_confidence = (
            sum(f.confidence for f in flows) / total_flows if total_flows > 0 else 0
        )

        flow_strength = (avg_amount / 100) * (avg_confidence / 100) * 100

        # Calculate flow momentum
        momentum = self._calculate_momentum(flows)

        # Group by asset class
        asset_class_flows = self._group_by_asset_class(flows)

        return {
            "status": "OPERATIONAL",
            "flow_count": total_flows,
            "total_inflow": total_inflow,
            "total_outflow": total_outflow,
            "net_flow": net_flow,
            "dominant_flow": dominant_flow,
            "flow_direction": direction,
            "flow_strength": min(100, flow_strength),
            "momentum": momentum.value,
            "asset_class_flows": asset_class_flows,
            "confidence": avg_confidence,
        }

    def _calculate_momentum(self, flows: list[CapitalFlowInput]) -> FlowMomentum:
        """Calculate flow momentum"""
        if len(flows) < 2:
            return FlowMomentum.STABLE

        # Compare current vs previous flow strength
        current_avg = sum(f.amount_normalized for f in flows) / len(flows)
        previous_avg = (
            sum(f.amount_normalized for f in flows[:-1]) / (len(flows) - 1)
            if len(flows) > 1
            else current_avg
        )

        if current_avg > previous_avg * 1.15:
            return FlowMomentum.ACCELERATING
        elif current_avg < previous_avg * 0.85:
            return FlowMomentum.DECELERATING
        elif (
            abs(current_avg - previous_avg) / previous_avg > 0.5
            if previous_avg > 0
            else False
        ):
            return FlowMomentum.REVERSING
        return FlowMomentum.STABLE

    def _group_by_asset_class(self, flows: list[CapitalFlowInput]) -> dict[str, float]:
        """Group flows by asset class"""
        asset_classes = {
            "XAUUSD": "COMMODITY",
            "XAGUSD": "COMMODITY",
            "WTI": "COMMODITY",
            "BRENT": "COMMODITY",
            "US500": "EQUITY",
            "US100": "EQUITY",
            "US30": "EQUITY",
            "GER40": "EQUITY",
            "UK100": "EQUITY",
            "JP225": "EQUITY",
            "EURUSD": "FX",
            "GBPUSD": "FX",
            "USDJPY": "FX",
            "AUDUSD": "FX",
            "NZDUSD": "FX",
            "USDCAD": "FX",
            "USDCHF": "FX",
        }

        class_flows = defaultdict(float)
        class_counts = defaultdict(int)

        for flow in flows:
            asset_class = asset_classes.get(flow.asset, "OTHER")
            class_flows[asset_class] += flow.amount_normalized * flow.confidence / 100
            class_counts[asset_class] += 1

        # Average by count
        for asset_class in class_flows:
            if class_counts[asset_class] > 0:
                class_flows[asset_class] = min(
                    100, class_flows[asset_class] / class_counts[asset_class]
                )

        return dict(class_flows)
