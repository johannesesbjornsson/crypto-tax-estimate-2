from abc import ABC, abstractmethod

from domain.models.currencies import Stablecoin, CryptoAsset, Currency


class CurrencyProvider(ABC):

    @abstractmethod
    def is_fiat(self, currency: str) -> bool:
        ...

    @abstractmethod
    def is_stablecoin(self, currency: str) -> bool:
        ...

    @abstractmethod
    def is_crypto_asset(self, currency: str) -> bool:
        ...

    def get_all_crypto_assets(self) -> list[CryptoAsset]:
        ...

    def get_all_stable_coins(self) -> list[Stablecoin]:
        ...

    def get_all_fiat_currencies(self) -> list[Currency]:
        ...