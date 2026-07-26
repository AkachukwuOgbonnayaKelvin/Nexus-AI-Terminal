"""Universal News DTO – used across all providers and layers."""

from datetime import datetime

from pydantic import BaseModel


class UniversalNews(BaseModel):
    article_id: str
    provider: str
    provider_article_id: str
    headline: str
    summary: str | None = None
    body: str | None = None
    url: str | None = None
    author: str | None = None
    country: str | None = None
    region: str | None = None
    language: str = "en"
    published_at: datetime
    updated_at: datetime | None = None
    category: str
    subcategory: str | None = None
    importance: str  # Critical, High, Medium, Low, Informational
    entities: list[str] = []
    assets: list[str] = []
    currencies: list[str] = []
    commodities: list[str] = []
    central_banks: list[str] = []
    governments: list[str] = []
    companies: list[str] = []
    tags: list[str] = []
    raw_payload: dict = {}
    confidence: float = 1.0
    metadata: dict = {}

    def to_dict(self) -> dict:
        return self.model_dump()
