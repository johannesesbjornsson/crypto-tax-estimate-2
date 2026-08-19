from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class KrakenTransaction:
    timestamp: datetime
    tx_id: str
    ref_id: str
    source: str

@dataclass
class KrakenTrade(KrakenTransaction):
    price: Decimal

    to_asset: str
    to_asset_amount: Decimal

    from_asset: str
    from_asset_amount: Decimal

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

