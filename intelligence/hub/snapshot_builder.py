"""
Global Intelligence Hub - Snapshot Builder
"""

import logging
import uuid
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class SnapshotBuilder:
    """
    Builds the final Global Intelligence Snapshot.
    """

    def build_snapshot(
        self,
        regime_report: Any,
        asset_report: Any,
        macro_report: Any,
        consensus: dict[str, Any],
        evidence_matrix: dict[str, Any],
        risk_matrix: dict[str, Any],
        executive_summary: str,
        ai_context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build the complete Global Intelligence Snapshot.
        """
        snapshot_id = (
            f"GI_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        )

        # Build confidence from consensus and reports
        confidence = self._calculate_confidence(
            regime_report, asset_report, macro_report, consensus
        )

        snapshot = {
            "snapshot_id": snapshot_id,
            "version": "1.0.0",
            "generated_at": datetime.utcnow().isoformat(),
            "workspace": "GLOBAL_INTELLIGENCE",
            # Core Intelligence
            "market_regime": self._extract_regime(regime_report),
            "macro_intelligence": self._extract_macro(macro_report),
            "asset_intelligence": self._extract_assets(asset_report),
            # Consensus & Confidence
            "consensus": consensus,
            "confidence": confidence,
            # Evidence & Risk
            "evidence_matrix": evidence_matrix,
            "risk_matrix": risk_matrix,
            # Executive Summary & AI Context
            "executive_summary": executive_summary,
            "ai_context": ai_context,
            # Health
            "health": self._build_health_status(
                regime_report, asset_report, macro_report
            ),
            "metadata": {
                "snapshot_version": "1.0.0",
                "engine_count": sum(
                    [
                        1 if regime_report else 0,
                        1 if asset_report else 0,
                        1 if macro_report else 0,
                    ]
                ),
            },
        }

        return snapshot

    def _calculate_confidence(
        self,
        regime_report: Any,
        asset_report: Any,
        macro_report: Any,
        consensus: dict[str, Any],
    ) -> dict[str, Any]:
        """Calculate confidence from available reports."""
        confidences = []
        components = {}

        # Extract confidence from regime report
        if regime_report and hasattr(regime_report, "confidence"):
            confidences.append(regime_report.confidence * 0.40)
            components["GLB-001"] = {
                "confidence": regime_report.confidence,
                "weight": 0.40,
            }

        # Extract confidence from asset report
        if asset_report and hasattr(asset_report, "confidence"):
            confidences.append(asset_report.confidence * 0.30)
            components["GLB-002"] = {
                "confidence": asset_report.confidence,
                "weight": 0.30,
            }

        # Extract confidence from macro report
        if macro_report and hasattr(macro_report, "confidence"):
            confidences.append(macro_report.confidence * 0.30)
            components["GLB-003"] = {
                "confidence": macro_report.confidence,
                "weight": 0.30,
            }

        if not confidences:
            return {
                "overall_confidence": 0.0,
                "status": "NO_CONFIDENCE_DATA",
                "components": components,
            }

        overall = sum(confidences)

        # Determine status
        if len(components) >= 3:
            status = "HIGH"
        elif len(components) >= 2:
            status = "MEDIUM"
        elif len(components) >= 1:
            status = "LOW"
        else:
            status = "NONE"

        return {
            "overall_confidence": overall,
            "status": status,
            "components": components,
        }

    def _extract_regime(self, report: Any) -> dict[str, Any]:
        if not report:
            return {"status": "NOT_AVAILABLE"}

        return {
            "primary_regime": report.primary_regime.value
            if hasattr(report, "primary_regime")
            else "UNKNOWN",
            "secondary_regime": report.secondary_regime.value
            if hasattr(report, "secondary_regime") and report.secondary_regime
            else None,
            "transition_state": report.transition_state.value
            if hasattr(report, "transition_state")
            else "STABLE",
            "regime_score": report.regime_score
            if hasattr(report, "regime_score")
            else 0,
            "confidence": report.confidence if hasattr(report, "confidence") else 0,
            "dimensions": report.dimensions if hasattr(report, "dimensions") else [],
            "drivers": report.drivers if hasattr(report, "drivers") else [],
            "risks": report.risks if hasattr(report, "risks") else [],
        }

    def _extract_macro(self, report: Any) -> dict[str, Any]:
        if not report:
            return {"status": "NOT_AVAILABLE"}

        return {
            "overall_score": report.overall_score
            if hasattr(report, "overall_score")
            else 0,
            "confidence": report.confidence if hasattr(report, "confidence") else 0,
            "signals": report.signals if hasattr(report, "signals") else [],
            "evidence": report.evidence if hasattr(report, "evidence") else [],
            "status": "OPERATIONAL",
        }

    def _extract_assets(self, report: Any) -> dict[str, Any]:
        if not report:
            return {"status": "NOT_AVAILABLE"}

        return {
            "assets": report.asset_reports if hasattr(report, "asset_reports") else {},
            "asset_count": len(report.asset_reports)
            if hasattr(report, "asset_reports")
            else 0,
            "status": "OPERATIONAL",
        }

    def _build_health_status(
        self, regime_report: Any, asset_report: Any, macro_report: Any
    ) -> dict[str, Any]:
        statuses = {
            "GLB-001": "OPERATIONAL" if regime_report else "MISSING",
            "GLB-002": "OPERATIONAL" if asset_report else "MISSING",
            "GLB-003": "OPERATIONAL" if macro_report else "MISSING",
        }

        is_healthy = all(s == "OPERATIONAL" for s in statuses.values())

        return {
            "status": "HEALTHY" if is_healthy else "DEGRADED",
            "engines": statuses,
            "operational_count": sum(
                1 for s in statuses.values() if s == "OPERATIONAL"
            ),
            "total_count": len(statuses),
        }
