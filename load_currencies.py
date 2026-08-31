from decimal import Decimal
import sys
from pathlib import Path
import zipfile

sys.path.insert(0, str(Path(__file__).parent / "src"))

from domain.models.currencies import Currency, Stablecoin, CryptoAsset

from database.session import get_session
from database.repositories.currency_repository import CurrencyRepository

def main():

    fiat_currencies = [
        Currency(code="USD", name="US Dollar"),
        Currency(code="GBP", name="British Pound"),
        Currency(code="EUR", name="Euro"),
    ]
    crypto_assets = [
        CryptoAsset(code="SOL", name="Solana"),
        CryptoAsset(code="BTC", name="Bitcoin"),
        CryptoAsset(code="ETH", name="Ethereum"),
        CryptoAsset(code="NEAR", name="Near Protocol"),
        CryptoAsset(code="AVAX", name="Avalanche"),
        CryptoAsset(code="DOT", name="Polkadot"),
        CryptoAsset(code="POL", name="Polygon"),
        CryptoAsset(code="MATIC", name="Polygon"),
        CryptoAsset(code="ARB", name="Arbitrum"),
        CryptoAsset(code="OP", name="Optimism"),
        CryptoAsset(code="ROSE", name="Oasis"),
        CryptoAsset(code="EGLD", name="Elrond"),

    ]

    stable_coins = [
        Stablecoin(code="USDT",peg_currency_code="USD",peg_ratio=Decimal(1),active=True),
        Stablecoin(code="BUSD",peg_currency_code="USD",peg_ratio=Decimal(1),active=True),
        Stablecoin(code="USDC",peg_currency_code="USD",peg_ratio=Decimal(1),active=True),
        Stablecoin(code="DAI",peg_currency_code="USD",peg_ratio=Decimal(1),active=True)
    ]


    
    session = get_session()
    repository = CurrencyRepository(session)
    try:
        for fiat in fiat_currencies:
            print(fiat)
            repository.save_fiat_currency(fiat)

        for asset in crypto_assets:
            repository.save_crypto_asset(asset)


        for stable_coin in stable_coins:
            repository.save_stable_coin(stable_coin)

        repository.commit()

    except Exception:
        session.rollback()
        raise
    
    finally:
        session.close()



if __name__ == "__main__":
    main()