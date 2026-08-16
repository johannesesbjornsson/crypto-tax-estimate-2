from dataclasses import dataclass
import datetime
from decimal import Decimal

from .transaction_type import TransactionType
from .transaction_source import TransactionSource

@dataclass
class Transaction:
    timestamp: datetime

    transaction_type: TransactionType

    asset: str
    amount: Decimal

    quote_asset: str | None
    quote_amount: Decimal | None

    price: Decimal | None

    fee_asset: str | None
    fee_amount: Decimal | None

    source: TransactionSource