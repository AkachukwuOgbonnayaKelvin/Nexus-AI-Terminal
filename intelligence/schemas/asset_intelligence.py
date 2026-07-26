"""Asset Intelligence Report Schema"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AssetClass(str, Enum):
    FX = "FX"
    COMMODITY = "COMMODITY"
    INDEX = "INDEX"
    EQUITY = "EQUITY"
    BOND = "BOND"
    CRYPTO = "CRYPTO"


class BiasDirection(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    MIXED = "MIXED"


@dataclass
class AssetDriver:
    """A driver influencing an asset"""

    name: str
    direction: BiasDirection
    score: float
    source_engine: str
    description: str | None = None


@dataclass
class AssetRisk:
    """A risk for an asset"""

    name: str
    severity: str
    probability: str
    description: str
    source_engine: str


@dataclass
class AssetIntelligenceReport:
    """
    Unified Asset Intelligence Report

    This is the standard format for intelligence about any asset.
    All sub-engines produce this format for asset-specific intelligence.
    """

    # REQUIRED fields (no defaults)
    report_id: str
    asset: str
    asset_class: AssetClass
    bias: BiasDirection
    engine_id: str
    engine_name: str

    # OPTIONAL fields with defaults
    score: float = 50.0
    confidence: float = 70.0

    # OPTIONAL with None default
    summary: str | None = None
    outlook: str | None = None

    # FACTORY defaults
    drivers: list[AssetDriver] = field(default_factory=list)
    risks: list[AssetRisk] = field(default_factory=list)
    supporting_engines: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "report_id": self.report_id,
            "asset": self.asset,
            "asset_class": self.asset_class.value,
            "bias": self.bias.value,
            "score": self.score,
            "confidence": self.confidence,
            "drivers": [
                {
                    "name": d.name,
                    "direction": d.direction.value,
                    "score": d.score,
                    "source_engine": d.source_engine,
                    "description": d.description,
                }
                for d in self.drivers
            ],
            "risks": [
                {
                    "name": r.name,
                    "severity": r.severity,
                    "probability": r.probability,
                    "description": r.description,
                    "source_engine": r.source_engine,
                }
                for r in self.risks
            ],
            "supporting_engines": self.supporting_engines,
            "engine_id": self.engine_id,
            "engine_name": self.engine_name,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "summary": self.summary,
            "outlook": self.outlook,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AssetIntelligenceReport":
        return cls(
            report_id=data["report_id"],
            asset=data["asset"],
            asset_class=AssetClass(data["asset_class"]),
            bias=BiasDirection(data["bias"]),
            engine_id=data["engine_id"],
            engine_name=data["engine_name"],
            score=data.get("score", 50.0),
            confidence=data.get("confidence", 70.0),
            summary=data.get("summary"),
            outlook=data.get("outlook"),
            drivers=[
                AssetDriver(
                    name=d["name"],
                    direction=BiasDirection(d["direction"]),
                    score=d["score"],
                    source_engine=d["source_engine"],
                    description=d.get("description"),
                )
                for d in data.get("drivers", [])
            ],
            risks=[
                AssetRisk(
                    name=r["name"],
                    severity=r["severity"],
                    probability=r["probability"],
                    description=r["description"],
                    source_engine=r["source_engine"],
                )
                for r in data.get("risks", [])
            ],
            supporting_engines=data.get("supporting_engines", []),
            timestamp=datetime.fromisoformat(data["timestamp"])
            if "timestamp" in data
            else datetime.now(),
            version=data.get("version", "1.0.0"),
            metadata=data.get("metadata", {}),
        )
