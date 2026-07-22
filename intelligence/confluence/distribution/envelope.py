"""
Phase 6: Distribution API - Output Envelope

Wraps outputs with metadata for routing and tracking.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Generic, TypeVar
from enum import Enum

T = TypeVar("T")


class OutputStatus(str, Enum):
    """Status of the output."""

    FINAL = "FINAL"
    SEMI_FINISHED = "SEMI_FINISHED"
    DRAFT = "DRAFT"
    ERROR = "ERROR"


class OutputType(str, Enum):
    """Type of output."""

    GLOBAL_INTELLIGENCE = "GLOBAL_INTELLIGENCE"
    ASSET_INTELLIGENCE_FEED = "ASSET_INTELLIGENCE_FEED"
    ENTITY_RATING = "ENTITY_RATING"
    ASSET_CLASS_RATING = "ASSET_CLASS_RATING"


@dataclass
class OutputEnvelope(Generic[T]):
    """
    Metadata wrapper for all Confluence outputs.

    Every output from the Confluence Engine should be wrapped
    in this envelope before being published.
    """

    # Message identification
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # Output metadata
    output_type: OutputType = OutputType.GLOBAL_INTELLIGENCE
    schema_version: str = "1.0.0"
    producer: str = "CONFLUENCE_ENGINE"

    # Status
    status: OutputStatus = OutputStatus.FINAL

    # Timestamps
    generated_at: datetime = field(default_factory=datetime.utcnow)
    valid_until: Optional[datetime] = None

    # Payload
    payload: Optional[T] = None

    # Additional metadata
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        """Set default valid_until if not provided."""
        if self.valid_until is None:
            self.valid_until = self.generated_at + timedelta(hours=1)

    def is_valid(self) -> bool:
        """Check if the envelope is still valid."""
        return datetime.utcnow() <= self.valid_until

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "message_id": self.message_id,
            "output_type": self.output_type.value,
            "schema_version": self.schema_version,
            "producer": self.producer,
            "status": self.status.value,
            "generated_at": self.generated_at.isoformat(),
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
            "payload": self.payload,
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        return (
            f"OutputEnvelope({self.message_id[:8]}, "
            f"type={self.output_type.value}, "
            f"status={self.status.value})"
        )


class EnvelopeFactory:
    """Factory for creating output envelopes."""

    @staticmethod
    def create_global_envelope(
        payload: T, metadata: Optional[dict] = None
    ) -> OutputEnvelope[T]:
        """
        Create a FINAL global intelligence envelope.

        Args:
            payload: GlobalIntelligenceOutput
            metadata: Additional metadata

        Returns:
            OutputEnvelope: Wrapped output
        """
        return OutputEnvelope(
            output_type=OutputType.GLOBAL_INTELLIGENCE,
            status=OutputStatus.FINAL,
            payload=payload,
            metadata=metadata or {},
        )

    @staticmethod
    def create_asset_feed_envelope(
        payload: T, symbol: str, metadata: Optional[dict] = None
    ) -> OutputEnvelope[T]:
        """
        Create a SEMI_FINISHED asset feed envelope.

        Args:
            payload: AssetIntelligenceFeed
            symbol: Asset symbol
            metadata: Additional metadata

        Returns:
            OutputEnvelope: Wrapped output
        """
        _metadata = metadata or {}
        _metadata["asset_symbol"] = symbol

        return OutputEnvelope(
            output_type=OutputType.ASSET_INTELLIGENCE_FEED,
            status=OutputStatus.SEMI_FINISHED,
            payload=payload,
            metadata=_metadata,
        )

    @staticmethod
    def create_asset_feeds_envelope(
        payloads: list, metadata: Optional[dict] = None
    ) -> list:
        """
        Create multiple asset feed envelopes.

        Args:
            payloads: List of AssetIntelligenceFeed
            metadata: Additional metadata

        Returns:
            list: List of OutputEnvelope
        """
        envelopes = []
        for payload in payloads:
            envelope = EnvelopeFactory.create_asset_feed_envelope(
                payload=payload, symbol=payload.symbol, metadata=metadata
            )
            envelopes.append(envelope)
        return envelopes
