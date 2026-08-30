from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from domain.models.exchange_rate import MarketPrice, ExchangeRate


class MarketPriceProvider(ABC):

    @abstractmethod
    def get_price(
        self,
        asset: str,
        quote_currency: str,
        timestamp: datetime,
    ) -> MarketPrice:
        pass