-- Sync state tracking for technical stores
CREATE TABLE IF NOT EXISTS technical_ohlc.sync_state (
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    last_synced_at TIMESTAMPTZ NOT NULL,
    last_raw_time TIMESTAMPTZ,
    last_technical_time TIMESTAMPTZ,
    raw_count INTEGER DEFAULT 0,
    technical_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'HEALTHY',
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, timeframe)
);
