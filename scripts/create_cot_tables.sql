-- COT Markets
CREATE TABLE IF NOT EXISTS cot_markets (
    market_code TEXT PRIMARY KEY,
    market_name TEXT,
    asset_class TEXT,
    currency TEXT,
    exchange TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- COT Reports
CREATE TABLE IF NOT EXISTS cot_reports (
    report_id TEXT,
    provider TEXT,
    report_date TIMESTAMPTZ,
    market_code TEXT REFERENCES cot_markets(market_code),
    open_interest INTEGER,
    confidence DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (report_id, market_code)
);

-- COT Positions
CREATE TABLE IF NOT EXISTS cot_positions (
    report_id TEXT,
    market_code TEXT REFERENCES cot_markets(market_code),
    participant_type TEXT,
    long_positions INTEGER,
    short_positions INTEGER,
    spreading_positions INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (report_id, market_code, participant_type)
);

-- COT Changes (for week-over-week differences)
CREATE TABLE IF NOT EXISTS cot_changes (
    report_id TEXT,
    market_code TEXT REFERENCES cot_markets(market_code),
    participant_type TEXT,
    long_change INTEGER,
    short_change INTEGER,
    spreading_change INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (report_id, market_code, participant_type)
);

-- Create indexes for performance
CREATE INDEX idx_cot_reports_date ON cot_reports (report_date DESC);
CREATE INDEX idx_cot_reports_market ON cot_reports (market_code);
CREATE INDEX idx_cot_positions_market ON cot_positions (market_code);
CREATE INDEX idx_cot_positions_type ON cot_positions (participant_type);
CREATE INDEX idx_cot_changes_market ON cot_changes (market_code);
