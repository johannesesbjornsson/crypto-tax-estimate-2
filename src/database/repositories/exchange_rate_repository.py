
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.models.exchange_rate import ExchangeRate
from domain.providers.exchange_rate_provider import ExchangeRateProvider

from database.models.exchange_rate import ExchangeRateModel


class ExchangeRateRepository(ExchangeRateProvider):

    def __init__(self, session: Session):
        self.session = session

    def save(self, exchange_rate: ExchangeRate):
        model = ExchangeRateModel(
            from_currency_code=exchange_rate.from_currency,
            to_currency_code=exchange_rate.to_currency,
            rate=exchange_rate.exchange_rate,
            timestamp=exchange_rate.timestamp,
            source=exchange_rate.source.source_file,
        )

        self.session.add(model)

    def get_rate(
        self,
        from_currency: str,
        to_currency: str,
        timestamp: datetime,
    ) -> ExchangeRate | None:

        statement = (
            select(ExchangeRateModel)
            .where(
                ExchangeRateModel.from_currency_code == from_currency,
                ExchangeRateModel.to_currency_code == to_currency,
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
            source=None,
            from_currency=model.from_currency_code,
            to_currency=model.to_currency_code,
            exchange_rate=model.rate,
        )

    def commit(self):
        self.session.commit()

