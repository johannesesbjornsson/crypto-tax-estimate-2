from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class KrakenTransaction:
    timestamp: datetime
    tx_id: str
    ref_id: str

@dataclass
class KrakenTrade(KrakenTransaction):
    pair: str
    side: str

    price: Decimal

    base_currency: str
    base_currency_amount: Decimal

    quote_currency: str
    quote_currency_amount: Decimal

    fee: Decimal
    fee_asset: str

@dataclass
class KrakenStaking(KrakenTransaction):
    asset: str
    amount: Decimal

@dataclass
class KrakenDeposit(KrakenTransaction):
    asset: str
    amount: Decimal

@dataclass
class KrakenWithdrawl(KrakenTransaction):
    asset: str
    amount: Decimal

