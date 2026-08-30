from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

from domain.models.exchange_rate import MarketPrice, ExchangeRate

class ExchangeRateProvider(ABC):

    @abstractmethod
    def get_rate(
        self,
        from_currency: str,
        to_currency: str,
        timestamp: datetime,
    ) -> ExchangeRate:
        pass