from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.models.exchange_rate import MarketPrice
from domain.providers.market_price_provider import MarketPriceProvider

from database.models.market_price import MarketPriceModel


class MarketPriceRepository(MarketPriceProvider):

    def __init__(self, session: Session):
        self.session = session

    def save(self, rate: MarketPrice):
        market_price = MarketPriceModel(
            asset_code=rate.asset,
            quote_currency_code=rate.quote_currency,
            price=rate.price,
            timestamp=rate.timestamp,
            interval=rate.interval,
            source=rate.source.source_file,
        )

        self.session.add(market_price)

    def get_price(
        self,
        asset: str,
        quote_currency: str,
        timestamp: datetime,
    ) -> MarketPrice | None:

        statement = (
            select(MarketPriceModel)
            .where(
                MarketPriceModel.asset_code == asset,
                MarketPriceModel.quote_currency_code == quote_currency,
                MarketPriceModel.interval == "1h",
                MarketPriceModel.timestamp <= timestamp,
            )
            .order_by(MarketPriceModel.timestamp.desc())
            .limit(1)
        )

        model = self.session.scalar(statement)

        if model is None:
            return None

        return MarketPrice(
            timestamp=model.timestamp,
            source=None,
            asset=model.asset_code,
            quote_currency=model.quote_currency_code,
            interval=model.interval,
            price=model.price,
        )

    def commit(self):
        self.session.commit()