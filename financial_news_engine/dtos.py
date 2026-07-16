"""Universal News DTO – used across all providers and layers."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UniversalNews(BaseModel):
    article_id: str
    provider: str
    provider_article_id: str
    headline: str
    summary: Optional[str] = None
    body: Optional[str] = None
    url: Optional[str] = None
    author: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    language: str = "en"
    published_at: datetime
    updated_at: Optional[datetime] = None
    category: str
    subcategory: Optional[str] = None
    importance: str  # Critical, High, Medium, Low, Informational
    entities: List[str] = []
    assets: List[str] = []
    currencies: List[str] = []
    commodities: List[str] = []
    central_banks: List[str] = []
    governments: List[str] = []
    companies: List[str] = []
    tags: List[str] = []
    raw_payload: dict = {}
    confidence: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
