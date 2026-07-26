-- Technical OHLC Store
CREATE SCHEMA IF NOT EXISTS technical_ohlc;

CREATE TABLE IF NOT EXISTS technical_ohlc.bars (
    symbol VARCHAR(20) NOT NULL,
    time TIMESTAMPTZ NOT NULL,
    timeframe VARCHAR(10) NOT NULL,
    open DECIMAL(20,8) NOT NULL,
    high DECIMAL(20,8) NOT NULL,
    low DECIMAL(20,8) NOT NULL,
    close DECIMAL(20,8) NOT NULL,
    volume DECIMAL(20,4) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, time, timeframe)
);

SELECT create_hypertable('technical_ohlc.bars', 'time', if_not_exists => TRUE);

-- Technical Microstructure Store
CREATE SCHEMA IF NOT EXISTS technical_microstructure;

CREATE TABLE IF NOT EXISTS technical_microstructure.ticks (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(20,8) NOT NULL,
    volume DECIMAL(20,4) DEFAULT 0,
    bid DECIMAL(20,8),
    ask DECIMAL(20,8),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, time)
);

SELECT create_hypertable('technical_microstructure.ticks', 'time', if_not_exists => TRUE);

CREATE INDEX IF NOT EXISTS idx_bars_timeframe ON technical_ohlc.bars(symbol, timeframe, time DESC);
CREATE INDEX IF NOT EXISTS idx_ticks_symbol ON technical_microstructure.ticks(symbol, time DESC);
