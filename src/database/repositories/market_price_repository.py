from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from domain.models.exchange_rate import MarketPrice

from database.models.market_price import MarketPriceModel
from domain.providers.market_price_provider import MarketPriceProvider
from domain.models.source import Source



class MarketPriceRepository(MarketPriceProvider):

    def __init__(self, session: Session):
        self.session = session

    def save(self, rate: MarketPrice):
        market_price = MarketPriceModel(
            asset=rate.asset,
            quote_currency=rate.quote_currency,
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
                MarketPriceModel.asset == asset,
                MarketPriceModel.quote_currency == quote_currency,
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
            source=Source(
                venue="tmp",
                source_file="tmp",
            ),
            asset=model.asset,
            quote_currency=model.quote_currency,
            interval=model.interval,
            price=model.price,
        )

    def commit(self):
        self.session.commit()