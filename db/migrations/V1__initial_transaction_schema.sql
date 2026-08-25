CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,

    venue_txn_id VARCHAR(255),
    timestamp TIMESTAMPTZ NOT NULL,
    venue VARCHAR(50) NOT NULL,
    source_file VARCHAR(255),
    checksum VARCHAR(64) NOT NULL,

    CONSTRAINT uq_transactions_venue_txn_id
        UNIQUE (venue, venue_txn_id),

    CONSTRAINT uq_transactions_checksum
        UNIQUE (checksum)
);

CREATE TABLE incomes (
    id BIGINT PRIMARY KEY
        REFERENCES transactions(id)
        ON DELETE CASCADE,
    asset VARCHAR(20) NOT NULL,
    amount NUMERIC(38, 18) NOT NULL
);

CREATE TABLE trades (
    id BIGINT PRIMARY KEY
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

CREATE TABLE deposits (
    id BIGINT PRIMARY KEY
        REFERENCES transactions(id)
        ON DELETE CASCADE,

    asset VARCHAR(20) NOT NULL,
    amount NUMERIC(38, 18) NOT NULL
);

CREATE TABLE withdrawals (
    id BIGINT PRIMARY KEY
        REFERENCES transactions(id)
        ON DELETE CASCADE,

    asset VARCHAR(20) NOT NULL,
    amount NUMERIC(38, 18) NOT NULL
);