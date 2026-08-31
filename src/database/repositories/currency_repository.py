

from sqlalchemy import select
from sqlalchemy.orm import Session


from domain.providers.currency_provider import CurrencyProvider
from domain.models.currencies import Currency, Stablecoin, CryptoAsset

from database.models.stablecoin import StablecoinModel
from database.models.currency import CurrencyModel
from database.models.crypto_asset import CryptoAssetModel


class CurrencyRepository(CurrencyProvider):
    def __init__(self, session: Session):
        self.session = session

    def is_fiat(self, currency_code: str) -> bool:
        statement = (select(CurrencyModel).where(CurrencyModel.code == currency_code))
        model = self.session.scalar(statement)

        if model:
            return True
        return False

    
    def is_stablecoin(self, currency_code: str) -> bool:
        statement = (select(StablecoinModel).where(StablecoinModel.code == currency_code))
        model = self.session.scalar(statement)

        if model:
            return True
        return False

    
    def is_crypto_asset(self, currency_code: str) -> bool:
        statement = (select(CryptoAssetModel).where(CryptoAssetModel.code == currency_code))
        model = self.session.scalar(statement)

        if model:
            return True
        return False

    def save_fiat_currency(self, asset: Currency):
        currency = CurrencyModel(
            code=asset.code,
            name=asset.name,
        )

        self.session.add(currency)
    
    def save_crypto_asset(self, asset: CryptoAsset):
        currency = CryptoAssetModel(
            code=asset.code,
            name=asset.name,
        )

        self.session.add(currency)

    def save_stable_coin(self, stable_coin: Stablecoin):
        currency = StablecoinModel(
            code=stable_coin.code,
            peg_currency_code=stable_coin.peg_currency_code,
            peg_ratio=stable_coin.peg_ratio,
            active=stable_coin.active,
        )

        self.session.add(currency)


    def commit(self):
        self.session.commit()