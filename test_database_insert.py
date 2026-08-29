import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.detection.detector import CSVFormatDetector

from database.session import get_session
from database.repositories.transaction_repository import TransactionRepository
from database.repositories.exchange_rate_repository import ExchangeRateRepository


def main():
    csv_file = Path("downloaded_files/kraken_2023-2024.csv")
    #csv_file = Path("downloaded_files/binance_2023-2024.csv")
    #csv_file = Path("downloaded_files/Bank of England  Database.csv")

    # Read CSV
    reader = CSVReader()
    document = reader.read(csv_file)

    # Detect format
    detector = CSVFormatDetector()
    parser = detector.detect(document)


    # Parse + normalise
    transactions = parser.parse(document)


    # Write to database
    session = get_session()

    try:
        repository = TransactionRepository(session)
        #repository = ExchangeRateRepository(session)

        for transaction in transactions:
            print(transaction)
            
            
            
            repository.save(transaction)


        repository.commit()

        

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()