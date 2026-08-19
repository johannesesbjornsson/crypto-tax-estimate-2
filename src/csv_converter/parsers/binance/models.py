from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class BinanceTransaction:
    timestamp: datetime

@dataclass
class BinanceTrade(BinanceTransaction):
    pair: str
    side: str

    price: Decimal

    base_currency: str
    base_currency_amount: Decimal

    quote_currency: str
    quote_currency_amount: Decimal

    fee: Decimal
    fee_asset: str

    source: str