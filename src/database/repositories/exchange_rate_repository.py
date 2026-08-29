from sqlalchemy.orm import Session

from domain.models.exchange_rate import ExchangeRate

from database.models.exchange_rate import ExchangeRateModel


class ExchangeRateRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, rate):
        if isinstance(rate, ExchangeRate):
            self._save_exchange_rate(rate)

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

    def commit(self):
        self.session.commit()