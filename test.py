import sys
from pathlib import Path

# Add src/ to Python's import path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.detection.detector import CSVFormatDetector


def main():
    #csv_file = Path("downloaded_files/binance_2021-2022.csv")
    csv_file = Path("downloaded_files/kraken_2023-2024.csv")

    # Read CSV
    reader = CSVReader()
    document = reader.read(csv_file)

    print("Headers:")
    print(document.headers)

    print(f"\nRows: {len(document.rows)}")

    # Detect format
    #detector = CSVFormatDetector(
    #    parsers=[
    #        BinanceTradeParser(),
    #    ]
    #)
    detector = CSVFormatDetector()
    parser = detector.detect(document)

    print(f"\nDetected parser: {type(parser).__name__}")

    # Parse
    trades = parser.parse(document)

    print(f"Parsed trades: {len(trades)}")


    for trade in trades:
        print(trade)


if __name__ == "__main__":
    main()