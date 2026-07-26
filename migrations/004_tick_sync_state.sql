CREATE TABLE IF NOT EXISTS technical_microstructure.sync_state (
    symbol TEXT PRIMARY KEY,
    last_raw_time TIMESTAMPTZ,
    last_synced_at TIMESTAMPTZ,
    raw_count INTEGER DEFAULT 0,
    technical_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'HEALTHY',
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
