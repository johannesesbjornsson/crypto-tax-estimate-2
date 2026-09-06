from datetime import datetime, timezone
from decimal import Decimal

import pytest

from domain.models.exchange_rate import ExchangeRate, MarketPrice
from domain.models.currencies import CryptoAsset, Currency, Stablecoin, WrappedCryptoAsset
from domain.models.transaction import Income, Trade
from services.valuation import ValuationService


class FakeMarketPriceProvider:

    def __init__(self, prices: list[MarketPrice]):
        self.prices = prices

    def get_price(self, asset: str, quote_currency: str, timestamp: datetime) -> MarketPrice | None:
        matches = [
            price
            for price in self.prices
            if (
                price.asset == asset
                and price.quote_currency == quote_currency
                and price.timestamp <= timestamp
            )
        ]

        if not matches:
            return None

        return max(
            matches,
            key=lambda price: price.timestamp,
        )
class FakeExchangeRateProvider:
    def __init__(self, rates: list[ExchangeRate]):
        self.rates = rates

    def get_rate(self, from_currency: str, to_currency: str, timestamp: datetime) -> ExchangeRate | None:
        matches = [
            rate
            for rate in self.rates
            if (
                rate.from_currency == from_currency
                and rate.to_currency == to_currency
                and rate.timestamp <= timestamp
            )
        ]

        if not matches:
            return None

        return max(
            matches,
            key=lambda price: price.timestamp,
        )



class FakeCurrencyProvider:

    def __init__(
        self,
        currencies: list[Currency],
        crypto_assets: list[CryptoAsset],
        stable_coins: list[Stablecoin],
        wrapped_crypto_assets: list[WrappedCryptoAsset]
    ):
        self._fiat_currencies = {
            currency.code: currency
            for currency in currencies
        }

        self._crypto_assets = {
            asset.code: asset
            for asset in crypto_assets
        }

        self._stablecoins = {
            stablecoin.code: stablecoin
            for stablecoin in stable_coins
        }
        self._wrapped_crypto_assets = {
            wrapped_crypto_asset.code : wrapped_crypto_asset
            for wrapped_crypto_asset in wrapped_crypto_assets

        }

    def is_fiat(self, currency_code: str) -> bool:
        return currency_code in self._fiat_currencies

    def is_stablecoin(self, currency_code: str) -> bool:
        return currency_code in self._stablecoins

    def is_crypto_asset(self, currency_code: str) -> bool: 
        all_assets = self._crypto_assets | self._wrapped_crypto_assets

        return currency_code in all_assets

    def is_wrapped_crypto_asset(self, currency_code: str) -> bool: 
        return currency_code in self._wrapped_crypto_assets
    
    def get_fiat_currency(self, currency_code: str) -> Currency | None:
        return self._fiat_currencies.get(currency_code)

    def get_stablecoin(self, currency_code: str) -> Stablecoin | None:
        return self._stablecoins.get(currency_code)

    def get_crypto_asset(self, currency_code: str) -> CryptoAsset | None:
        return self._crypto_assets.get(currency_code)

    def get_underlying_asset(self, wrapped_crypto_asset_code: str) -> CryptoAsset:
        underlying_asset = self._wrapped_crypto_assets.get(wrapped_crypto_asset_code)
        if underlying_asset is None:
            raise ValueError(f"No crypto asset found {wrapped_crypto_asset_code}")
        
        return underlying_asset


@pytest.fixture
def valuation_service():
    market_prices = [
        MarketPrice(
            timestamp=datetime(2024, 3, 5, 6, 0, tzinfo=timezone.utc),
            source=None,
            asset="SOL",
            quote_currency="USDT",
            interval="1h",
            price=Decimal("150"),
        ),
        MarketPrice(
            timestamp=datetime(2024, 3, 5, 7, 0, tzinfo=timezone.utc),
            source=None,
            asset="SOL",
            quote_currency="USDT",
            interval="1h",
            price=Decimal("155"),
        ),
        MarketPrice(
            timestamp=datetime(2024, 3, 6, 6, 0, tzinfo=timezone.utc),
            source=None,
            asset="SOL",
            quote_currency="USDT",
            interval="1h",
            price=Decimal("155"),
        ),
        MarketPrice(
            timestamp=datetime(2024, 3, 6, 7, 0, tzinfo=timezone.utc),
            source=None,
            asset="SOL",
            quote_currency="USDT",
            interval="1h",
            price=Decimal("155"),
        ),
    ]

    exchange_rates = [
        ExchangeRate(
            timestamp=datetime(2024, 3, 5, 0, 0, tzinfo=timezone.utc),
            source=None,
            from_currency="GBP",
            to_currency="USD",
            exchange_rate=Decimal("1.25"),
        ),
        ExchangeRate(
            timestamp=datetime(2024, 3, 6, 0, 0, tzinfo=timezone.utc),
            source=None,
            from_currency="GBP",
            to_currency="USD",
            exchange_rate=Decimal("1.30"),
        ),
    ]
    currencies = [
        Currency(code="USD", name="US Dollar"),
        Currency(code="GBP", name="British Pound")
    ]
    crypto_assets = [
        CryptoAsset(code="SOL", name="Solana"),
        CryptoAsset(code="BTC", name="Bitcoin"),
        CryptoAsset(code="ETH", name="Ethereum"),
        CryptoAsset(code="ADA", name="Cardano")

    ]

    wrapped_crypto_assets = []

    stable_coins = [
        Stablecoin(code="USDT",peg_currency_code="USD",peg_ratio=Decimal(1),active=True)
    ]
    

    return ValuationService(
        fiat_currency=Currency(code="GBP", name="British Pound"),
        market_price_provider=FakeMarketPriceProvider(market_prices),
        exchange_rate_provider=FakeExchangeRateProvider(exchange_rates),
        currency_provider=FakeCurrencyProvider(stable_coins=stable_coins, currencies=currencies, crypto_assets=crypto_assets, wrapped_crypto_assets=wrapped_crypto_assets)
    )

def test_income(valuation_service):

    income_1 = Income(
        timestamp=datetime(2024, 3, 5, 6, 43, tzinfo=timezone.utc),
        source=None,
        venue_txn_id=None,
        asset="SOL",
        amount=Decimal(0.1),
    )
    income_2 = Income(
        timestamp=datetime(2024, 3, 5, 7, 43, tzinfo=timezone.utc),
        source=None,
        venue_txn_id=None,
        asset="SOL",
        amount=Decimal(0.1),
    )
    income_3 = Income(
        timestamp=datetime(2024, 3, 6, 7, 43, tzinfo=timezone.utc),
        source=None,
        venue_txn_id=None,
        asset="SOL",
        amount=Decimal(0.1),
    )

    valued_transaction_1 = valuation_service.value_transaction(income_1)

    assert valued_transaction_1.asset == "SOL"
    assert valued_transaction_1.amount == Decimal(0.1)
    assert valued_transaction_1.fiat_value == Decimal('12.00000000000000066613381478') 

    valued_transaction_2 = valuation_service.value_transaction(income_2)

    assert valued_transaction_2.asset == "SOL"
    assert valued_transaction_2.amount == Decimal(0.1)
    assert valued_transaction_2.fiat_value == Decimal('12.40000000000000068833827527')

    valued_transaction_3 = valuation_service.value_transaction(income_3)

    assert valued_transaction_3.asset == "SOL"
    assert valued_transaction_3.amount == Decimal(0.1)
    assert valued_transaction_3.fiat_value == Decimal('11.92307692307692373878680314')

def test_acquisition(valuation_service):
    trade_1 = Trade(
        from_asset="USDT",
        from_asset_amount=Decimal(150),
        to_asset="SOL",
        to_asset_amount=Decimal(1),
        timestamp=datetime(2024, 3, 5, 6, 0, tzinfo=timezone.utc),
        fee_asset="USDT",
        fee_amount=Decimal(1),
        exchange_rate=Decimal(150),
        source=None,
        venue_txn_id=None,
    )
    trade_2 = Trade(
        from_asset="USDT",
        from_asset_amount=Decimal(155),
        to_asset="SOL",
        to_asset_amount=Decimal(1),
        timestamp=datetime(2024, 3, 6, 6, 0, tzinfo=timezone.utc),
        fee_asset="USDT",
        fee_amount=Decimal(1),
        exchange_rate=Decimal(150),
        source=None,
        venue_txn_id=None,
    )
    trade_3 = Trade(
        from_asset="SOL",
        from_asset_amount=Decimal(2),
        to_asset="USDT",
        to_asset_amount=Decimal(310),
        timestamp=datetime(2024, 3, 6, 7, 20, tzinfo=timezone.utc),
        fee_asset="USDT",
        fee_amount=Decimal(1),
        exchange_rate=Decimal(0.006451),
        source=None,
        venue_txn_id=None,
    )

    valued_transaction_1 = valuation_service.value_transaction(trade_1)
    assert valued_transaction_1.fiat_value == Decimal('120')
    assert valued_transaction_1.fiat_price == Decimal('120')

    valued_transaction_2 = valuation_service.value_transaction(trade_2)
    assert valued_transaction_2.fiat_value == Decimal('119.2307692307692307692307692')
    assert valued_transaction_2.fiat_price == Decimal('119.2307692307692307692307692')    

    valued_transaction_3 = valuation_service.value_transaction(trade_3)

    assert valued_transaction_3.fiat_value == Decimal('238.4615384615384615384615384')
    assert valued_transaction_3.fiat_price == Decimal('119.2307692307692307692307692')


