"""Base Intelligence Engine - Universal lifecycle contract"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from intelligence.schemas.engine_report import EngineReport, ReportStatus
from intelligence.schemas.evidence import Evidence
from intelligence.schemas.intelligence_signal import IntelligenceSignal
from intelligence.schemas.risk import Risk

logger = logging.getLogger(__name__)


class IntelligenceEngine(ABC):
    """
    Universal Base Intelligence Engine.

    All intelligence engines (GLB-001 to GLB-008) must inherit from this class.
    This ensures every engine follows the same lifecycle and produces the same
    standardized output format.

    Lifecycle:
    1. validate_input() - Check if input data is valid
    2. normalize() - Normalize data to internal format
    3. analyze() - Perform core analysis
    4. collect_evidence() - Gather supporting evidence
    5. calculate_score() - Calculate overall score
    6. evaluate_risk() - Identify and assess risks
    7. generate_signals() - Generate intelligence signals
    8. create_report() - Produce standardized Engine Report
    """

    def __init__(self, engine_id: str, engine_name: str, domain: str = "global"):
        self.engine_id = engine_id
        self.engine_name = engine_name
        self.domain = domain
        self.version = "1.0.0"
        self._signals: list[IntelligenceSignal] = []
        self._evidence: list[Evidence] = []
        self._risks: list[Risk] = []
        self._top_drivers: list[dict[str, Any]] = []
        self._overall_score: float = 50.0
        self._confidence: float = 70.0
        self._direction: str | None = None
        self._risk_level: str | None = None
        self._regime: str | None = None
        self._summary: str = ""
        self._recommendations: list[str] = []

    @abstractmethod
    def validate_input(self, data: dict[str, Any]) -> bool:
        """
        Validate that input data is complete and correct.

        Args:
            data: Raw input data from NDIP

        Returns:
            True if valid, False otherwise
        """

    @abstractmethod
    def normalize(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Normalize input data to internal format.

        Args:
            data: Raw input data from NDIP

        Returns:
            Normalized data dictionary
        """

    @abstractmethod
    def analyze(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Perform core analysis on normalized data.

        Args:
            data: Normalized data

        Returns:
            Analysis results
        """

    @abstractmethod
    def collect_evidence(self, data: dict[str, Any]) -> list[Evidence]:
        """
        Collect supporting evidence from the analysis.

        Args:
            data: Analysis results

        Returns:
            List of Evidence objects
        """

    @abstractmethod
    def calculate_score(self, data: dict[str, Any]) -> float:
        """
        Calculate overall score (0-100).

        Args:
            data: Analysis results

        Returns:
            Score between 0 and 100
        """

    @abstractmethod
    def evaluate_risk(self, data: dict[str, Any]) -> list[Risk]:
        """
        Identify and assess risks.

        Args:
            data: Analysis results

        Returns:
            List of Risk objects
        """

    @abstractmethod
    def generate_signals(self, data: dict[str, Any]) -> list[IntelligenceSignal]:
        """
        Generate intelligence signals from analysis.

        Args:
            data: Analysis results

        Returns:
            List of IntelligenceSignal objects
        """

    @abstractmethod
    def get_required_ndip_topics(self) -> list[str]:
        """
        Return list of NDIP topics this engine consumes.

        Returns:
            List of topic names
        """

    @abstractmethod
    def get_engine_scope(self) -> dict[str, Any]:
        """
        Return the engine's scope (region, assets, time horizon).

        Returns:
            Scope dictionary
        """

    def run(self, input_data: dict[str, Any]) -> EngineReport:
        """
        Universal engine lifecycle.

        This is the main entry point for the engine.
        It orchestrates the entire analysis pipeline.
        """
        try:
            # Step 1: Validate input
            if not self.validate_input(input_data):
                return self._create_error_report("Input validation failed")

            # Step 2: Normalize data
            normalized = self.normalize(input_data)

            # Step 3: Analyze
            analysis = self.analyze(normalized)

            # Step 4: Collect evidence
            self._evidence = self.collect_evidence(analysis)

            # Step 5: Calculate score
            self._overall_score = self.calculate_score(analysis)

            # Step 6: Evaluate risk
            self._risks = self.evaluate_risk(analysis)

            # Step 7: Generate signals
            self._signals = self.generate_signals(analysis)

            # Step 8: Create report
            return self.create_report()

        except Exception as e:
            logger.error(f"Engine {self.engine_id} failed: {e}")
            return self._create_error_report(str(e))

    def create_report(self) -> EngineReport:
        """
        Create standardized Engine Report.

        Returns:
            EngineReport object
        """
        return EngineReport(
            report_id=f"{self.engine_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            engine_id=self.engine_id,
            engine_name=self.engine_name,
            domain=self.domain,
            version=self.version,
            status=ReportStatus.SUCCESS,
            scope=self.get_engine_scope(),
            overall_score=self._overall_score,
            confidence=self._confidence,
            direction=self._direction,
            risk_level=self._risk_level,
            regime=self._regime,
            signals=self._signals,
            evidence=self._evidence,
            risks=self._risks,
            top_drivers=self._top_drivers,
            summary=self._summary,
            recommendations=self._recommendations,
            timestamp=datetime.now(),
        )

    def _create_error_report(self, error_message: str) -> EngineReport:
        """
        Create an error report when the engine fails.

        Args:
            error_message: Description of the error

        Returns:
            EngineReport with error status
        """
        return EngineReport(
            report_id=f"{self.engine_id}_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            engine_id=self.engine_id,
            engine_name=self.engine_name,
            domain=self.domain,
            version=self.version,
            status=ReportStatus.ERROR,
            scope=self.get_engine_scope(),
            overall_score=0.0,
            confidence=0.0,
            summary=f"Engine failed: {error_message}",
            timestamp=datetime.now(),
        )

    def add_evidence(self, evidence: Evidence):
        """Add supporting evidence"""
        self._evidence.append(evidence)

    def add_signal(self, signal: IntelligenceSignal):
        """Add an intelligence signal"""
        self._signals.append(signal)

    def add_risk(self, risk: Risk):
        """Add a risk"""
        self._risks.append(risk)

    def add_driver(self, name: str, impact: str, score: float):
        """Add a top driver"""
        self._top_drivers.append({"driver": name, "impact": impact, "score": score})

    def add_recommendation(self, recommendation: str):
        """Add a recommendation"""
        self._recommendations.append(recommendation)

    def set_confidence(self, confidence: float):
        """Set the confidence level"""
        self._confidence = min(100.0, max(0.0, confidence))

    def set_direction(self, direction: str):
        """Set the direction (BULLISH/BEARISH/NEUTRAL)"""
        self._direction = direction

    def set_risk_level(self, risk_level: str):
        """Set the risk level (LOW/MEDIUM/HIGH/CRITICAL)"""
        self._risk_level = risk_level

    def set_regime(self, regime: str):
        """Set the regime (RISK_ON/RISK_OFF/NEUTRAL)"""
        self._regime = regime

    def set_summary(self, summary: str):
        """Set the summary"""
        self._summary = summary
