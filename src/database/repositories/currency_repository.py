from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.currency import CurrencyModel
from database.models.stablecoin import StablecoinModel
from database.models.crypto_asset import CryptoAssetModel

from domain.models.currencies import Currency, Stablecoin, CryptoAsset
from domain.providers.currency_provider import CurrencyProvider


class CurrencyRepository(CurrencyProvider):

    def __init__(self, session: Session):
        self.session = session

        self._fiat_currencies: dict[str, Currency] = {}
        self._stablecoins: dict[str, Stablecoin] = {}
        self._crypto_assets: dict[str, CryptoAsset] = {}

        self._load_currencies()

    def _load_currencies(self) -> None:
        fiat_models = self.session.scalars(
            select(CurrencyModel)
        ).all()

        self._fiat_currencies = {
            model.code: Currency(
                code=model.code,
                name=model.name,
            )
            for model in fiat_models
        }

        stablecoin_models = self.session.scalars(
            select(StablecoinModel)
        ).all()

        self._stablecoins = {
            model.code: Stablecoin(
                code=model.code,
                peg_currency_code=model.peg_currency_code,
                peg_ratio=model.peg_ratio,
                active=model.active,
            )
            for model in stablecoin_models
        }

        # Crypto assets
        crypto_models = self.session.scalars(
            select(CryptoAssetModel)
        ).all()

        self._crypto_assets = {
            model.code: CryptoAsset(
                code=model.code,
                name=model.name,
            )
            for model in crypto_models
        }

    def is_fiat(self, currency_code: str) -> bool:
        return currency_code in self._fiat_currencies

    def is_stablecoin(self, currency_code: str) -> bool:
        return currency_code in self._stablecoins

    def is_crypto_asset(self, currency_code: str) -> bool:
        return currency_code in self._crypto_assets

    def get_fiat_currency(self, currency_code: str) -> Currency | None:
        return self._fiat_currencies.get(currency_code)

    def get_stablecoin(self, currency_code: str) -> Stablecoin | None:
        return self._stablecoins.get(currency_code)

    def get_crypto_asset(self, currency_code: str) -> CryptoAsset | None:
        return self._crypto_assets.get(currency_code)

    def save_fiat_currency(self, asset: Currency) -> None:
        model = CurrencyModel(
            code=asset.code,
            name=asset.name,
        )

        self.session.add(model)

        self._fiat_currencies[asset.code] = asset

    def save_crypto_asset(self, asset: CryptoAsset) -> None:
        model = CryptoAssetModel(
            code=asset.code,
            name=asset.name,
        )

        self.session.add(model)

        self._crypto_assets[asset.code] = asset

    def save_stable_coin(self, stable_coin: Stablecoin) -> None:
        model = StablecoinModel(
            code=stable_coin.code,
            peg_currency_code=stable_coin.peg_currency_code,
            peg_ratio=stable_coin.peg_ratio,
            active=stable_coin.active,
        )

        self.session.add(model)
        self._stablecoins[stable_coin.code] = stable_coin

    def commit(self) -> None:
        self.session.commit()
