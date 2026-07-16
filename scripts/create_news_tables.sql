CREATE TABLE IF NOT EXISTS news_articles (
    article_id TEXT PRIMARY KEY,
    provider TEXT,
    provider_article_id TEXT,
    headline TEXT,
    summary TEXT,
    body TEXT,
    url TEXT,
    author TEXT,
    country TEXT,
    region TEXT,
    language TEXT,
    published_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    category TEXT,
    subcategory TEXT,
    importance TEXT,
    tags TEXT[],
    confidence DOUBLE PRECISION,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_news_published ON news_articles (published_at DESC);
CREATE INDEX idx_news_importance ON news_articles (importance);
CREATE INDEX idx_news_category ON news_articles (category);

-- Additional tables for entities, assets, duplicates can be added later.
