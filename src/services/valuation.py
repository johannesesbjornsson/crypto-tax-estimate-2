from decimal import Decimal

from domain.models.transaction import (
    Transaction,
    Income,
    Trade,
)

from domain.providers.exchange_rate_provider import ExchangeRateProvider
from domain.providers.market_price_provider import MarketPriceProvider
from domain.providers.currency_provider import CurrencyProvider
from domain.models.currencies import Currency


from domain.models.valuation import (
    ValuatedTransaction,
    ValuatedIncome,
    Disposal,
    Acquisition,
    Swap,
    StableCoinAcquisition,
    StableCoinDisposal
)


class ValuationService:

    def __init__(self, 
            fiat_currency: Currency,
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
        if self.currency_provider.is_crypto_asset(income.asset):
            pass
        elif self.currency_provider.is_stablecoin(income.asset):
            raise NotImplementedError("Not implemented for stablecoin income")
        else:
            raise ValueError(f"Unknown asset: {income.asset}")
        
        
        market_price = self.market_price_provider.get_price(
            asset=income.asset,
            quote_currency="USDT",
            timestamp=income.timestamp,
        )

        if market_price is None:
            raise ValueError(f"No market price found for {income.asset}/USDT at {income.timestamp}")

        if self.fiat_currency.code != "USD":
            exchange_rate = self.exchange_rate_provider.get_rate(
                from_currency=self.fiat_currency.code,
                to_currency="USD",
                timestamp=income.timestamp,
            )

            if exchange_rate is None:
                raise ValueError(f"No exchange rate found for {self.fiat_currency}/USD at {income.timestamp}")

            fiat_value = income.amount * (market_price.price / exchange_rate.exchange_rate)
        else:
            fiat_value = income.amount * market_price.price

        return ValuatedIncome(
            timestamp=income.timestamp,
            fiat_currency=self.fiat_currency,
            asset=income.asset,
            amount=income.amount,
            fiat_value=Decimal(fiat_value),
        )

    def _process_acquisition(self, trade: Trade) -> Acquisition:
        if trade.from_asset == self.fiat_currency.code:
            fiat_price = Decimal(trade.from_asset_amount / trade.to_asset_amount)
            fiat_value = Decimal(fiat_price*trade.to_asset_amount)

        elif self.currency_provider.is_stablecoin(trade.from_asset):
            exchange_rate = self.exchange_rate_provider.get_rate(
                from_currency=self.fiat_currency.code,
                to_currency="USD",
                timestamp=trade.timestamp,
            )

            if exchange_rate is None:
                raise ValueError(f"No exchange rate found for {self.fiat_currency.code}/USD at {trade.timestamp}")

            fiat_price = Decimal((trade.from_asset_amount / trade.to_asset_amount) / exchange_rate.exchange_rate)
            fiat_value = Decimal(fiat_price*trade.to_asset_amount)

        else:
            raise ValueError(f"Unable to value acquisition, from {trade.from_asset} to {trade.to_asset}")

        return Acquisition(
            timestamp=trade.timestamp,
            fiat_currency=self.fiat_currency,
            asset=trade.to_asset,
            amount=trade.to_asset_amount,
            fiat_value=fiat_value,
            fiat_price=fiat_price
        )
    
    def _process_stable_coin_acquisition(self, trade: Trade) -> StableCoinAcquisition:
        stablecoin = self.currency_provider.get_stablecoin(trade.to_asset)

        if stablecoin is None:
            raise ValueError(f"Unable to find stablecoin {trade.to_asset}")
        usd_value = trade.to_asset_amount * stablecoin.peg_ratio
            

        if self.fiat_currency.code == "USD":
            fiat_value = usd_value
        else:
            exchange_rate = self.exchange_rate_provider.get_rate(
                from_currency=self.fiat_currency.code,
                to_currency="USD",
                timestamp=trade.timestamp,
            )

            if exchange_rate is None:
                raise ValueError(f"No exchange rate found for {self.fiat_currency.code}/USD at {trade.timestamp}")

            fiat_value = usd_value / exchange_rate.exchange_rate

        fiat_price = fiat_value / trade.to_asset_amount

        return StableCoinAcquisition(
            timestamp=trade.timestamp,
            fiat_currency=self.fiat_currency,
            asset=trade.to_asset,
            amount=trade.to_asset_amount,
            fiat_value=fiat_value,
            fiat_price=fiat_price,
        )


    def _process_disposal(self, trade: Trade) -> Disposal:
        if self.currency_provider.is_crypto_asset(trade.from_asset):
            market_price = self.market_price_provider.get_price(
                asset=trade.from_asset,
                quote_currency="USDT",
                timestamp=trade.timestamp,
            )

            if market_price is None:
                raise ValueError(f"No market price found for {trade.from_asset}/USDT at {trade.timestamp}")

            if self.fiat_currency.code == "USD":
                fiat_price = market_price.price
            else:
                exchange_rate = self.exchange_rate_provider.get_rate(
                    from_currency=self.fiat_currency.code,
                    to_currency="USD",
                    timestamp=trade.timestamp,
                )

                if exchange_rate is None:
                    raise ValueError(
                        f"No exchange rate found for "
                        f"{self.fiat_currency.code}/USD at {trade.timestamp}"
                    )

                fiat_price = market_price.price / exchange_rate.exchange_rate

            fiat_value = trade.from_asset_amount * fiat_price

        elif self.currency_provider.is_stablecoin(trade.from_asset):
            stablecoin = self.currency_provider.get_stablecoin(
                trade.from_asset
            )

            if stablecoin is None:
                raise ValueError(f"Unable to find stablecoin {trade.from_asset}")

            usd_value = trade.from_asset_amount * stablecoin.peg_ratio
                

            if self.fiat_currency.code == "USD":
                fiat_value = usd_value
            else:
                exchange_rate = self.exchange_rate_provider.get_rate(
                    from_currency=self.fiat_currency.code,
                    to_currency="USD",
                    timestamp=trade.timestamp,
                )

                if exchange_rate is None:
                    raise ValueError(f"No exchange rate found for {self.fiat_currency.code}/USD at {trade.timestamp}")

                fiat_value = usd_value / exchange_rate.exchange_rate

            fiat_price = fiat_value / trade.from_asset_amount

        else:
            raise ValueError(f"Unable to value disposal of {trade.from_asset}")

        return Disposal(
            timestamp=trade.timestamp,
            fiat_currency=self.fiat_currency,
            asset=trade.from_asset,
            amount=trade.from_asset_amount,
            fiat_value=fiat_value,
            fiat_price=fiat_price,
        )


    def _process_swap(self, trade: Trade) -> Swap:
        if not self.currency_provider.is_crypto_asset(trade.from_asset):
            raise ValueError(f"Unable to swap non-crypto asset {trade.from_asset}")

        if not self.currency_provider.is_crypto_asset(trade.to_asset):
            raise ValueError(f"Unable to swap to non-crypto asset {trade.to_asset}")

        market_price = self.market_price_provider.get_price(
            asset=trade.from_asset,
            quote_currency="USDT",
            timestamp=trade.timestamp,
        )

        if market_price is None:
            raise ValueError(f"No market price found for {trade.from_asset}/USDT at {trade.timestamp}")

        if self.fiat_currency.code == "USD":
            disposed_fiat_price = market_price.price
        else:
            exchange_rate = self.exchange_rate_provider.get_rate(
                from_currency=self.fiat_currency.code,
                to_currency="USD",
                timestamp=trade.timestamp,
            )

            if exchange_rate is None:
                raise ValueError(f"No exchange rate found for {self.fiat_currency.code}/USD at {trade.timestamp}")

            disposed_fiat_price = market_price.price / exchange_rate.exchange_rate

        disposed_fiat_value = trade.from_asset_amount * disposed_fiat_price
            

        acquired_fiat_value = disposed_fiat_value
        acquired_fiat_price = acquired_fiat_value / trade.to_asset_amount
            

        return Swap(
            timestamp=trade.timestamp,
            fiat_currency=self.fiat_currency,
            disposed_asset=trade.from_asset,
            disposed_amount=trade.from_asset_amount,
            disposed_fiat_value=disposed_fiat_value,
            disposed_fiat_price=disposed_fiat_price,
            acquired_asset=trade.to_asset,
            acquired_amount=trade.to_asset_amount,
            acquired_fiat_value=acquired_fiat_value,
            acquired_fiat_price=acquired_fiat_price,
        )

    def _process_stable_coin_disposal(self, trade: Trade) -> StableCoinDisposal:
        stablecoin = self.currency_provider.get_stablecoin(
            trade.from_asset
        )

        if stablecoin is None:
            raise ValueError(f"Unable to find stablecoin {trade.from_asset}")

        usd_value = trade.from_asset_amount * stablecoin.peg_ratio
            

        if self.fiat_currency.code == "USD":
            fiat_value = usd_value
        else:
            exchange_rate = self.exchange_rate_provider.get_rate(
                from_currency=self.fiat_currency.code,
                to_currency="USD",
                timestamp=trade.timestamp,
            )

            if exchange_rate is None:
                raise ValueError(f"No exchange rate found for {self.fiat_currency.code}/USD at {trade.timestamp}")

            fiat_value = usd_value / exchange_rate.exchange_rate

        fiat_price = fiat_value / trade.from_asset_amount

        return StableCoinDisposal(
            timestamp=trade.timestamp,
            fiat_currency=self.fiat_currency,
            asset=trade.from_asset,
            amount=trade.from_asset_amount,
            fiat_value=fiat_value,
            fiat_price=fiat_price,
        )



    def _process_trade(self, trade: Trade) -> ValuatedTransaction:
        if trade.from_asset == self.fiat_currency.code and self.currency_provider.is_stablecoin(trade.to_asset):
            return self._process_stable_coin_acquisition(trade)

        elif self.currency_provider.is_stablecoin(trade.from_asset) and trade.to_asset == self.fiat_currency.code:
            return self._process_stable_coin_disposal(trade)

        elif trade.from_asset == self.fiat_currency.code or self.currency_provider.is_stablecoin(trade.from_asset):
            return self._process_acquisition(trade)

        elif trade.to_asset == self.fiat_currency.code or self.currency_provider.is_stablecoin(trade.to_asset):
            return self._process_disposal(trade)

        elif self.currency_provider.is_crypto_asset(trade.from_asset) and self.currency_provider.is_crypto_asset(trade.to_asset):
            return self._process_swap(trade)

        else:
            raise ValueError(f"Unable to process trade from {trade.from_asset} to {trade.to_asset}")

