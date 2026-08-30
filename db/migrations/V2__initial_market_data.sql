CREATE TABLE market_prices (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    asset VARCHAR(20) NOT NULL,
    quote_currency VARCHAR(10) NOT NULL,
    price NUMERIC(38, 18) NOT NULL,
    source VARCHAR(50) NOT NULL,
    interval VARCHAR(20) NOT NULL,

    UNIQUE (timestamp, asset, quote_currency, source)
);


CREATE TABLE exchange_rates (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    from_currency VARCHAR(10) NOT NULL,
    to_currency VARCHAR(10) NOT NULL,
    rate NUMERIC(38, 18) NOT NULL,
    source VARCHAR(50) NOT NULL,

    UNIQUE (timestamp, from_currency, to_currency)
);

CREATE INDEX idx_market_prices_lookup
    ON market_prices (asset, quote_currency, timestamp);

CREATE INDEX idx_exchange_rates_lookup
    ON exchange_rates (from_currency, to_currency, timestamp);


CREATE TABLE currencies (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL
);

INSERT INTO currencies (code, name, type)
VALUES
    ('USD', 'US Dollar', 'FIAT'),
    ('GBP', 'British Pound', 'FIAT'),
    ('EUR', 'Euro', 'FIAT');


CREATE TABLE stablecoins (
    asset VARCHAR(20) PRIMARY KEY,
    peg_currency VARCHAR(10) NOT NULL,
    peg_ratio NUMERIC(38, 18) NOT NULL DEFAULT 1,
    active BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (peg_currency)
        REFERENCES currencies(code)
);
INSERT INTO stablecoins (asset, peg_currency, peg_ratio)
VALUES
    ('USDT', 'USD', 1),
    ('USDC', 'USD', 1),
    ('BUSD', 'USD', 1),
    ('DAI',  'USD', 1),
    ('FDUSD', 'USD', 1);