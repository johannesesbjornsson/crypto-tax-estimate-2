import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.detection.detector import CSVFormatDetector

from database.session import get_session
from database.repositories.exchange_rate_repository import ExchangeRateRepository


def main():
    csv_files = [
        Path("downloaded_files/Bank of England  Database.csv")
    ]
    

    # Write to database
    session = get_session()
    for csv_file in csv_files:
        reader = CSVReader()
        document = reader.read(csv_file)
        detector = CSVFormatDetector()
        parser = detector.detect(document)
        transactions = parser.parse(document)
        try:
            
            repository = ExchangeRateRepository(session)

            for transaction in transactions:
                #print(transaction)


                repository.save(transaction)


            repository.commit()



        except Exception:
            session.rollback()
            raise

        finally:
            session.close()


if __name__ == "__main__":
    main()