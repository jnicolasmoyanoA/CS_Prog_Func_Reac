CREATE TABLE IF NOT EXISTS active_candles (
    id SERIAL PRIMARY KEY,
    token TEXT NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    close_time TIMESTAMPTZ NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC,
    is_closed BOOLEAN,
    updated_at BIGINT
);

CREATE TABLE IF NOT EXISTS closed_candles (
    token TEXT NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    close_time TIMESTAMPTZ NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC,
    PRIMARY KEY (token, open_time)
);

CREATE INDEX IF NOT EXISTS idx_active_updated_at ON active_candles (updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_closed_token_time ON closed_candles (token, open_time DESC);