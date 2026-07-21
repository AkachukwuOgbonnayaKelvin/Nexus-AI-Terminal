# -*- coding: utf-8 -*-
"""Base Auditor for Raw Backend Certification"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class AuditResult:
    """Result of a single audit check"""

    name: str
    status: str  # PASS, FAIL, WARNING, SKIP
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    expected: Optional[Any] = None
    actual: Optional[Any] = None


@dataclass
class EngineCertification:
    """Certification result for a single engine"""

    engine_id: str
    engine_name: str
    status: str  # CERTIFIED, PARTIAL, FAILED
    checks: List[AuditResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    records: Dict[str, int] = field(default_factory=dict)  # provider, warehouse, ndip


class BaseAuditor(ABC):
    """Base class for raw backend auditors"""

    def __init__(self, engine_id: str):
        self.engine_id = engine_id
        self.results: List[AuditResult] = []

    @abstractmethod
    def audit_provider(self) -> AuditResult:
        """Audit provider data acquisition"""
        pass

    @abstractmethod
    def audit_warehouse(self) -> AuditResult:
        """Audit warehouse storage"""
        pass

    @abstractmethod
    def audit_ndip(self) -> AuditResult:
        """Audit NDIP publication"""
        pass

    @abstractmethod
    def audit_lineage(self) -> AuditResult:
        """Audit data lineage"""
        pass

    @abstractmethod
    def audit_parity(self) -> AuditResult:
        """Audit provider ↔ warehouse ↔ ndip parity"""
        pass

    @abstractmethod
    def audit_idempotency(self) -> AuditResult:
        """Audit duplicate prevention"""
        pass

    def run_all(self) -> EngineCertification:
        """Run all audits and return certification"""
        checks = []

        # Run each audit
        for audit_name in [
            "audit_provider",
            "audit_warehouse",
            "audit_ndip",
            "audit_lineage",
            "audit_parity",
            "audit_idempotency",
        ]:
            try:
                result = getattr(self, audit_name)()
                checks.append(result)
            except Exception as e:
                checks.append(
                    AuditResult(
                        name=audit_name, status="FAIL", message=f"Audit error: {e}"
                    )
                )

        # Determine status
        failed = [c for c in checks if c.status == "FAIL"]
        if failed:
            status = "FAILED"
        elif any(c.status == "WARNING" for c in checks):
            status = "PARTIAL"
        else:
            status = "CERTIFIED"

        return EngineCertification(
            engine_id=self.engine_id,
            engine_name=self._get_engine_name(),
            status=status,
            checks=checks,
        )

    def _get_engine_name(self) -> str:
        """Get engine name from engine_id"""
        names = {
            "MKT-001": "Market Price Engine",
            "MAC-001": "Macroeconomic Statistics Engine",
            "ECO-002": "Corporate Earnings Engine",
            "INS-001": "Institutional Positioning Engine",
            "CENT-001": "Central Bank Engine",
        }
        return names.get(self.engine_id, self.engine_id)
