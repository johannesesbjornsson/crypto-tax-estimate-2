from datetime import datetime, timezone
from decimal import Decimal

import pytest

from domain.models.exchange_rate import ExchangeRate, MarketPrice
from domain.models.source import Source
from domain.models.transaction import Income
from domain.models.valuation import ValuatedIncome
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
    ]

    exchange_rates = [
        ExchangeRate(
            timestamp=datetime(2024, 3, 5, 0, 0, tzinfo=timezone.utc),
            source=None,
            from_currency="GBP",
            to_currency="USD",
            exchange_rate=Decimal("1.25"),
        ),
    ]

    return ValuationService(
        fiat_currency="GBP",
        market_price_provider=FakeMarketPriceProvider(market_prices),
        exchange_rate_provider=FakeExchangeRateProvider(exchange_rates),
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

    valued_transaction_1 = valuation_service.value_transaction(income_1)

    assert valued_transaction_1.asset == "SOL"
    assert valued_transaction_1.amount == Decimal(0.1)
    assert valued_transaction_1.fiat_value == Decimal('12.00000000000000066613381478') 

    valued_transaction_2 = valuation_service.value_transaction(income_2)

    assert valued_transaction_2.asset == "SOL"
    assert valued_transaction_2.amount == Decimal(0.1)
    assert valued_transaction_2.fiat_value == Decimal('12.40000000000000068833827527') 


