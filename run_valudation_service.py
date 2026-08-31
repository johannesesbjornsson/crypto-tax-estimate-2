import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.detection.detector import CSVFormatDetector

from database.session import get_session
from database.repositories.market_price_repository import MarketPriceRepository
from database.repositories.exchange_rate_repository import ExchangeRateRepository
from database.repositories.currency_repository import CurrencyRepository
from services.valuation import ValuationService

from domain.models.transaction import (
    Transaction,
    Income,
    Trade,
)

def main():

    csv_files = [
        Path("downloaded_files/kraken_2023-2024.csv"),
        Path("downloaded_files/binance_2023-2024.csv"),
    ]
    


    session = get_session()
    md_repository = MarketPriceRepository(session)
    exchange_rate_repository = ExchangeRateRepository(session)
    currency_repository = CurrencyRepository(session)

    vaulation_service = ValuationService(
        fiat_currency="GBP",
        market_price_provider=md_repository,
        exchange_rate_provider=exchange_rate_repository,
        currency_provider=currency_repository
    )
    
    # Write to database
    
    for csv_file in csv_files:
        reader = CSVReader()
        document = reader.read(csv_file)
        detector = CSVFormatDetector()
        parser = detector.detect(document)


        transactions = parser.parse(document)

        try:

            for txn in transactions:
                if not isinstance(txn, Income) and not isinstance(txn, Trade):
                    continue
                if isinstance(txn, Trade):
                    continue
                if txn.asset  != "SOL":
                    continue

                valuated_txn = vaulation_service.value_transaction(txn)
                print(valuated_txn)



        except Exception:
            session.rollback()
            raise

        finally:
            session.close()


if __name__ == "__main__":
    main()