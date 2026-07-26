"""Universal Central Bank Event DTO."""

from datetime import datetime

from pydantic import BaseModel


class UniversalCentralBankEvent(BaseModel):
    event_id: str
    provider: str
    bank: str
    country: str
    currency: str
    event_type: str  # RateDecision, Minutes, Speech, PressConference, etc.
    title: str
    summary: str | None = None
    statement: str | None = None
    release_time: datetime
    meeting_date: datetime | None = None
    effective_date: datetime | None = None
    old_rate: float | None = None
    new_rate: float | None = None
    rate_change: float | None = None
    vote_split: str | None = None
    governor: str | None = None
    importance: str  # Critical, High, Medium, Low
    policy_bias: str | None = None  # Hawkish, Neutral, Dovish, Unknown
    hawkish_dovish_score: float | None = None
    communication_type: (
        str  # Speech, Statement, Minutes, PressConference, Interview, Testimony
    )
    source_url: str | None = None
    attachments: list[str] = []
    document_hash: str | None = None
    confidence: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
