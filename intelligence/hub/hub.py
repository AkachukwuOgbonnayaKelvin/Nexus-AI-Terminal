"""
Global Intelligence Hub - Main Hub Class
"""

import logging
from datetime import datetime
from typing import Any

from .ai_context_builder import AIContextBuilder
from .confidence_engine import ConfidenceEngine
from .consensus_engine import ConsensusEngine
from .evidence_matrix_builder import EvidenceMatrixBuilder
from .executive_summary_generator import ExecutiveSummaryGenerator
from .report_collector import ReportCollector
from .risk_matrix_builder import RiskMatrixBuilder
from .snapshot_builder import SnapshotBuilder

logger = logging.getLogger(__name__)


class GlobalIntelligenceHub:
    """
    Global Intelligence Hub - Central aggregator for all global intelligence.
    """

    def __init__(self):
        self.report_collector = ReportCollector()
        self.consensus_engine = ConsensusEngine()
        self.confidence_engine = ConfidenceEngine()
        self.evidence_builder = EvidenceMatrixBuilder()
        self.risk_builder = RiskMatrixBuilder()
        self.executive_summary_generator = ExecutiveSummaryGenerator()
        self.ai_context_builder = AIContextBuilder()
        self.snapshot_builder = SnapshotBuilder()

        self.last_snapshot: dict[str, Any] | None = None
        self.last_run_time: datetime | None = None

    def collect_report(self, engine_id: str, report: Any) -> bool:
        """
        Collect a report from a Global Intelligence engine.
        """
        return self.report_collector.collect_report(engine_id, report)

    def build_snapshot(self) -> dict[str, Any]:
        """
        Build the complete Global Intelligence Snapshot.
        """
        # Get all reports
        reports = self.report_collector.get_all_reports()
        regime_report = reports.get("GLB-001")
        asset_report = reports.get("GLB-002")
        macro_report = reports.get("GLB-003")

        # Calculate consensus
        consensus = self.consensus_engine.calculate_consensus(reports)

        # Calculate confidence (using the confidence engine)
        # confidence = ...

        # Build evidence matrix
        evidence_matrix = self.evidence_builder.build_matrix(reports)

        # Build risk matrix
        risk_matrix = self.risk_builder.build_matrix(reports)

        # Generate executive summary
        executive_summary = self.executive_summary_generator.generate(
            regime_report, asset_report, macro_report, consensus
        )

        # Build AI context
        ai_context = self.ai_context_builder.build(
            regime_report, asset_report, macro_report, consensus
        )

        # Build final snapshot
        snapshot = self.snapshot_builder.build_snapshot(
            regime_report=regime_report,
            asset_report=asset_report,
            macro_report=macro_report,
            consensus=consensus,
            evidence_matrix=evidence_matrix,
            risk_matrix=risk_matrix,
            executive_summary=executive_summary,
            ai_context=ai_context,
        )

        self.last_snapshot = snapshot
        self.last_run_time = datetime.utcnow()

        logger.info(f"Global Intelligence Snapshot built: {snapshot['snapshot_id']}")

        return snapshot

    def get_last_snapshot(self) -> dict[str, Any] | None:
        """Get the last built snapshot."""
        return self.last_snapshot

    def health_check(self) -> dict[str, Any]:
        """Check hub health."""
        status = self.report_collector.get_collection_status()

        return {
            "hub_id": "GLOBAL_INTELLIGENCE_HUB",
            "status": "OPERATIONAL",
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "has_snapshot": self.last_snapshot is not None,
            "collection_status": status,
        }
