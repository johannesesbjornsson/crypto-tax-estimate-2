from sqlalchemy.orm import Session

from domain.models.exchange_rate import ExchangeRate, MarketPrice

from database.models.exchange_rate import ExchangeRateModel
from database.models.market_price import MarketPriceModel


class ExchangeRateRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, rate):
        if isinstance(rate, ExchangeRate):
            self._save_exchange_rate(rate)
        elif isinstance(rate, MarketPrice):
            self._save_market_price(rate)

        else:
            raise ValueError(
                f"Unsupported type: "
                f"{type(rate).__name__}"
            )
    def _save_exchange_rate(self, rate: ExchangeRate):
        exchange_rate = ExchangeRateModel(
            from_currency=rate.from_currency,
            to_currency=rate.to_currency,
            rate=rate.exchange_rate,
            timestamp=rate.timestamp,
            source=rate.source.source_file,
        )

        self.session.add(exchange_rate)

    def _save_market_price(self, rate: MarketPrice):
        exchange_rate = MarketPriceModel(
            asset=rate.asset,
            quote_currency=rate.quote_currency,
            price=rate.price,
            timestamp=rate.timestamp,
            interval=rate.interval,
            source=rate.source.source_file,
        )

        self.session.add(exchange_rate)

    def commit(self):
        self.session.commit()