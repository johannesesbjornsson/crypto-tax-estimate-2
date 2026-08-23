import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.detection.detector import CSVFormatDetector

from database.session import get_session
from database.repository import TransactionRepository


def main():
    csv_file = Path("downloaded_files/kraken_2023-2024.csv")

    # Read CSV
    reader = CSVReader()
    document = reader.read(csv_file)

    print("Headers:")
    print(document.headers)

    print(f"\nRows: {len(document.rows)}")

    # Detect format
    detector = CSVFormatDetector()
    parser = detector.detect(document)

    print(f"\nDetected parser: {type(parser).__name__}")

    # Parse + normalize
    transactions = parser.parse(document)

    print(f"Parsed transactions: {len(transactions)}")

    # Write to database
    session = get_session()

    try:
        repository = TransactionRepository(session)

        for transaction in transactions:
            print(transaction)
            if transaction:
                repository.save(transaction)


        repository.commit()

        print(f"\nSaved {len(transactions)} transactions")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    main()