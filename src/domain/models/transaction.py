from dataclasses import dataclass
import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class TransactionSource:
    venue: str
    source_file: Optional[str]

@dataclass
class Transaction:
    id: str
    timestamp: datetime
    source: TransactionSource

@dataclass
class Income(Transaction):
    asset: str
    amount: str


@dataclass
class Trade(Transaction):
    from_asset: str
    from_asset_amount: Decimal

    to_asset: str 
    to_asset_amount: Decimal 

    fee_asset: str
    fee_amount: Decimal

    exchange_rate: Decimal