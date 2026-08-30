from dataclasses import dataclass
from decimal import Decimal
import datetime

@dataclass
class ValuatedTransaction:
    timestamp: datetime
    fiat_currency: str

@dataclass
class ValuatedIncome(ValuatedTransaction):
    asset: str
    amount: Decimal
    fiat_value: Decimal


@dataclass
class Disposal(ValuatedTransaction):
    asset: str
    amount: Decimal
    fiat_value: Decimal

@dataclass
class Acquisition(ValuatedTransaction):
    asset: str
    amount: Decimal
    fiat_value: Decimal


@dataclass
class Swap(ValuatedTransaction):

    disposed_asset: str
    disposed_amount: Decimal
    disposed_fiat_value: Decimal

    acquired_asset: str
    acquired_amount: Decimal
    acquired_fiat_value: Decimal
