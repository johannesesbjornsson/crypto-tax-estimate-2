from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Currency:
    code: str
    name: str

@dataclass
class Stablecoin:
    code: str
    peg_currency_code: str
    peg_ratio: Decimal
    active: bool

@dataclass
class CryptoAsset:
    code: str
    name: str

@dataclass
class WrappedCryptoAsset:
    code: str
    name: str
    underlying_asset_code: str
