"""Universal Central Bank Event DTO."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UniversalCentralBankEvent(BaseModel):
    event_id: str
    provider: str
    bank: str
    country: str
    currency: str
    event_type: str  # RateDecision, Minutes, Speech, PressConference, etc.
    title: str
    summary: Optional[str] = None
    statement: Optional[str] = None
    release_time: datetime
    meeting_date: Optional[datetime] = None
    effective_date: Optional[datetime] = None
    old_rate: Optional[float] = None
    new_rate: Optional[float] = None
    rate_change: Optional[float] = None
    vote_split: Optional[str] = None
    governor: Optional[str] = None
    importance: str  # Critical, High, Medium, Low
    policy_bias: Optional[str] = None  # Hawkish, Neutral, Dovish, Unknown
    hawkish_dovish_score: Optional[float] = None
    communication_type: (str)  # Speech, Statement, Minutes, PressConference, Interview, Testimony
    source_url: Optional[str] = None
    attachments: List[str] = []
    document_hash: Optional[str] = None
    confidence: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
