CREATE TABLE currencies (
    code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE stablecoins (
    code VARCHAR(20) PRIMARY KEY,
    peg_currency VARCHAR(10) NOT NULL,
    peg_ratio NUMERIC(38, 18) NOT NULL DEFAULT 1,
    active BOOLEAN NOT NULL DEFAULT TRUE,

    FOREIGN KEY (peg_currency)
        REFERENCES currencies(code)
);


CREATE TABLE crypto_assets (
    code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE market_prices (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,

    asset_code VARCHAR(20) NOT NULL,
    quote_currency_code VARCHAR(20) NOT NULL,

    price NUMERIC(38, 18) NOT NULL,
    source VARCHAR(255),
    interval VARCHAR(20) NOT NULL,

    FOREIGN KEY (asset_code)
        REFERENCES crypto_assets(code),

    FOREIGN KEY (quote_currency_code)
        REFERENCES stablecoins(code),

    UNIQUE (timestamp, asset_code, quote_currency_code, source)
);


CREATE TABLE exchange_rates (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    from_currency VARCHAR(10) NOT NULL,
    to_currency VARCHAR(10) NOT NULL,
    rate NUMERIC(38, 18) NOT NULL,
    source VARCHAR(50) NOT NULL,

    FOREIGN KEY (from_currency)
        REFERENCES currencies(code),

    FOREIGN KEY (to_currency)
        REFERENCES currencies(code),

    UNIQUE (timestamp, from_currency, to_currency)
);


CREATE INDEX idx_market_prices_lookup
    ON market_prices (asset_code, quote_currency_code, timestamp);


CREATE INDEX idx_exchange_rates_lookup
    ON exchange_rates (from_currency, to_currency, timestamp);