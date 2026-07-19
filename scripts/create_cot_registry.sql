-- COT Market Registry
CREATE TABLE IF NOT EXISTS cot_market_registry (
    market_code TEXT PRIMARY KEY,
    market_name TEXT,
    exchange TEXT,
    asset_class TEXT,
    currency TEXT,
    contract_size INTEGER,
    tick_size DECIMAL,
    first_seen DATE,
    last_seen DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- COT Reports
CREATE TABLE IF NOT EXISTS cot_reports (
    report_id TEXT PRIMARY KEY,
    report_date DATE,
    report_type TEXT,
    source TEXT,
    downloaded_at TIMESTAMPTZ DEFAULT NOW()
);

-- COT Positions
CREATE TABLE IF NOT EXISTS cot_positions (
    position_id SERIAL PRIMARY KEY,
    report_id TEXT REFERENCES cot_reports(report_id),
    market_code TEXT REFERENCES cot_market_registry(market_code),
    report_type TEXT,
    participant_type TEXT,
    long_positions INTEGER,
    short_positions INTEGER,
    spreading_positions INTEGER,
    change_long INTEGER,
    change_short INTEGER,
    change_spreading INTEGER,
    open_interest INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Import Log
CREATE TABLE IF NOT EXISTS cot_import_log (
    log_id SERIAL PRIMARY KEY,
    run_date TIMESTAMPTZ DEFAULT NOW(),
    report_date DATE,
    markets_processed INTEGER,
    records_inserted INTEGER,
    errors INTEGER,
    status TEXT
);

-- Provider Health
CREATE TABLE IF NOT EXISTS cot_provider_health (
    provider TEXT PRIMARY KEY,
    status TEXT,
    last_sync TIMESTAMPTZ,
    records INTEGER,
    latency_ms INTEGER,
    error_message TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Statistics
CREATE TABLE IF NOT EXISTS cot_statistics (
    stat_id SERIAL PRIMARY KEY,
    market_code TEXT REFERENCES cot_market_registry(market_code),
    report_date DATE,
    total_reports INTEGER,
    avg_open_interest INTEGER,
    max_open_interest INTEGER,
    min_open_interest INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_cot_positions_report ON cot_positions (report_id);
CREATE INDEX idx_cot_positions_market ON cot_positions (market_code);
CREATE INDEX idx_cot_positions_date ON cot_positions (report_date);
CREATE INDEX idx_cot_reports_date ON cot_reports (report_date DESC);
CREATE INDEX idx_cot_market_registry_active ON cot_market_registry (is_active);
CREATE INDEX idx_cot_market_registry_class ON cot_market_registry (asset_class);
