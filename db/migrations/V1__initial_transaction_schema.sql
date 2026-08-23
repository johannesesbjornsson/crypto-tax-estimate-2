CREATE TABLE transactions (
    id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    venue VARCHAR(50) NOT NULL,
    source_file VARCHAR(255)
);

CREATE TABLE income (
    id VARCHAR(255) PRIMARY KEY
        REFERENCES transactions(id)
        ON DELETE CASCADE,
    asset VARCHAR(20) NOT NULL,
    amount NUMERIC(38, 18) NOT NULL
);

CREATE TABLE trades (
    id VARCHAR(255)  PRIMARY KEY
        REFERENCES transactions(id)
        ON DELETE CASCADE,
    from_asset VARCHAR(20) NOT NULL,
    from_asset_amount NUMERIC(38, 18) NOT NULL,
    to_asset VARCHAR(20) NOT NULL,
    to_asset_amount NUMERIC(38, 18) NOT NULL,
    fee_asset VARCHAR(20) NOT NULL,
    fee_amount NUMERIC(38, 18) NOT NULL,
    exchange_rate NUMERIC(38, 18) NOT NULL
);