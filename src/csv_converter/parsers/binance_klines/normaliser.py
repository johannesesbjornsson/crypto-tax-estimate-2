from domain.models.exchange_rate import MarketPrice
from domain.models.source import Source
from .models import BinanceKline

class BinanceKlineNormaliser:

    def normalise(self, exchange_rate: BinanceKline) -> MarketPrice:

        if isinstance(exchange_rate, BinanceKline):
            return self.normalise_market_price(exchange_rate)

        raise ValueError(
            f"Unsupported Kraken transaction: "
            f"{type(exchange_rate).__name__}"
        )


    def normalise_market_price(self, exchange_rate: BinanceKline) -> MarketPrice:
        return MarketPrice(
            timestamp=exchange_rate.open_time,   
            asset=exchange_rate.asset,
            quote_currency=exchange_rate.quote_currency,
            price=exchange_rate.open,
            interval="1h",
            source=Source(
                venue="binance",
                source_file=exchange_rate.source_file
            ), 
        )