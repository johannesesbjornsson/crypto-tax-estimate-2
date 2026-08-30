from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.models.exchange_rate import ExchangeRate
from domain.models.source import Source
from domain.providers.exchange_rate_provider import ExchangeRateProvider

from database.models.exchange_rate import ExchangeRateModel


class ExchangeRateRepository(ExchangeRateProvider):

    def __init__(self, session: Session):
        self.session = session

    def save(self, rate: ExchangeRate):
        exchange_rate = ExchangeRateModel(
            from_currency=rate.from_currency,
            to_currency=rate.to_currency,
            rate=rate.exchange_rate,
            timestamp=rate.timestamp,
            source=rate.source.source_file,
        )

        self.session.add(exchange_rate)

    def get_rate(
        self,
        from_currency: str,
        to_currency: str,
        timestamp: datetime,
    ) -> ExchangeRate | None:

        statement = (
            select(ExchangeRateModel)
            .where(
                ExchangeRateModel.from_currency == from_currency,
                ExchangeRateModel.to_currency == to_currency,
                ExchangeRateModel.timestamp <= timestamp,
            )
            .order_by(ExchangeRateModel.timestamp.desc())
            .limit(1)
        )

        model = self.session.scalar(statement)

        if model is None:
            return None

        return ExchangeRate(
            timestamp=model.timestamp,
            source=Source(
                venue="tmp",
                source_file="tmp",
            ),
            from_currency=model.from_currency,
            to_currency=model.to_currency,
            exchange_rate=model.rate,
        )

    def commit(self):
        self.session.commit()