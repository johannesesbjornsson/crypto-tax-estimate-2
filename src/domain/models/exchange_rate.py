from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from .source import Source

@dataclass
class ExchangeRate:
    timestamp: datetime
    source: Source
    from_currency: str
    to_currency: str
    exchange_rate: Decimal


@dataclass
class MarketPrice:
    timestamp: datetime
    source: Source
    asset: str
    quote_currency: str
    interval: str
    price: Decimal
    

