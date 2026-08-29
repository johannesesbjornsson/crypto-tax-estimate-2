from dataclasses import dataclass
import datetime
from decimal import Decimal
from .source import Source
import hashlib



@dataclass
class Transaction:
    venue_txn_id: str | None
    timestamp: datetime
    source: Source

@dataclass
class Income(Transaction):
    asset: str
    amount: Decimal
    @property
    def checksum(self) -> str:
        data = "|".join([
            self.timestamp.isoformat(),
            self.source.venue,
            str(self.amount),
            self.asset,
            
        ])

        return hashlib.sha256(data.encode("utf-8")).hexdigest()


@dataclass
class Trade(Transaction):
    from_asset: str
    from_asset_amount: Decimal

    to_asset: str 
    to_asset_amount: Decimal 

    fee_asset: str
    fee_amount: Decimal

    exchange_rate: Decimal

    @property
    def checksum(self) -> str:
        data = "|".join([
            self.timestamp.isoformat(),
            self.source.venue,
            self.from_asset,
            str(self.from_asset_amount),
            self.to_asset,
            str(self.to_asset_amount),
            self.fee_asset,
            str(self.fee_amount),
            str(self.exchange_rate),
        ])

        return hashlib.sha256(data.encode("utf-8")).hexdigest()

@dataclass
class Deposit(Transaction):
    asset: str
    amount: Decimal
    
    @property
    def checksum(self) -> str:
        data = "|".join([
            self.timestamp.isoformat(),
            self.source.venue,
            str(self.amount),
            self.asset,
            
        ])

        return hashlib.sha256(data.encode("utf-8")).hexdigest()


@dataclass
class Withdrawl(Transaction):
    asset: str
    amount: Decimal
    @property
    def checksum(self) -> str:
        data = "|".join([
            self.timestamp.isoformat(),
            self.source.venue,
            str(self.amount),
            self.asset,
            
        ])

        return hashlib.sha256(data.encode("utf-8")).hexdigest()
    