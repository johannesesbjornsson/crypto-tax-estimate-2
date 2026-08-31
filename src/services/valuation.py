from decimal import Decimal

from domain.models.transaction import (
    Transaction,
    Income,
    Trade,
)

from domain.providers.exchange_rate_provider import ExchangeRateProvider
from domain.providers.market_price_provider import MarketPriceProvider
from domain.providers.currency_provider import CurrencyProvider


from domain.models.valuation import (
    ValuatedTransaction,
    ValuatedIncome,
    Disposal,
    Acquisition,
    Swap,
)


class ValuationService:

    def __init__(self, 
            fiat_currency: str,
            market_price_provider: MarketPriceProvider,
            exchange_rate_provider: ExchangeRateProvider,
            currency_provider: CurrencyProvider,
        ):
        self.fiat_currency = fiat_currency
        self.market_price_provider = market_price_provider
        self.exchange_rate_provider = exchange_rate_provider
        self.currency_provider = currency_provider

    def value_transaction(self, transaction: Transaction):
        if isinstance(transaction, Trade):
            return self._process_trade(transaction)

        elif isinstance(transaction, Income):
            return self._process_income(transaction)

        else:
            raise ValueError(
                f"Unsupported transaction type: "
                f"{type(transaction).__name__}"
            )
  


    def _process_income(self, income: Income) -> ValuatedIncome:
        market_price = self.market_price_provider.get_price(
            asset=income.asset,
            quote_currency="USDT",
            timestamp=income.timestamp,
        )
        exchange_rate = self.exchange_rate_provider.get_rate(
            from_currency=self.fiat_currency,
            to_currency="USD",
            timestamp=income.timestamp,
        )

        if market_price is None:
            raise ValueError(
                f"No market price found for {income.asset}/USDT "
                f"at {income.timestamp}"
            )
        
        if exchange_rate is None:
            raise ValueError(
                f"No exchange rate found for "
                f"{self.fiat_currency}/USD at {income.timestamp}"
            )
        fiat_value = income.amount * (market_price.price/exchange_rate.exchange_rate)

        return ValuatedIncome(
            timestamp=income.timestamp,
            fiat_currency=self.fiat_currency,
            asset=income.asset,
            amount=income.amount,
            fiat_value=Decimal(fiat_value),
        )
        
    def _process_trade(self, trade: Trade):
        pass
