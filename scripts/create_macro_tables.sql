-- Raw events (audit trail)
CREATE TABLE IF NOT EXISTS macro_events_raw (
    raw_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider TEXT,
    provider_event_id TEXT,
    country TEXT,
    currency TEXT,
    title TEXT,
    category TEXT,
    forecast DOUBLE PRECISION,
    previous DOUBLE PRECISION,
    actual DOUBLE PRECISION,
    importance TEXT,
    release_time_utc TIMESTAMPTZ,
    status TEXT,
    raw_data JSONB,
    ingested_at TIMESTAMPTZ DEFAULT NOW()
);

-- Consensus events (published)
CREATE TABLE IF NOT EXISTS macro_events_consensus (
    event_id TEXT PRIMARY KEY,
    country TEXT,
    currency TEXT,
    title TEXT,
    category TEXT,
    subcategory TEXT,
    forecast DOUBLE PRECISION,
    previous DOUBLE PRECISION,
    actual DOUBLE PRECISION,
    consensus DOUBLE PRECISION,
    revised_previous DOUBLE PRECISION,
    importance TEXT,
    impact_score INTEGER,
    release_time_utc TIMESTAMPTZ,
    status TEXT,
    source_url TEXT,
    tags TEXT[],
    affected_assets TEXT[],
    confidence DOUBLE PRECISION,
    quality_score DOUBLE PRECISION,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

SELECT create_hypertable('macro_events_consensus', 'release_time_utc', if_not_exists => TRUE);

CREATE INDEX idx_macro_consensus_country ON macro_events_consensus (country);
CREATE INDEX idx_macro_consensus_category ON macro_events_consensus (category);
CREATE INDEX idx_macro_consensus_release ON macro_events_consensus (release_time_utc DESC);
