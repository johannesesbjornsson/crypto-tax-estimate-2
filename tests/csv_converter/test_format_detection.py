from csv_converter.reader.csv_reader import CSVReader
from csv_converter.detection.detector import CSVFormatDetector
from pathlib import Path
from csv_converter.parsers.kraken.transaction import KrakenTransactionParser
from csv_converter.parsers.binance.trade import BinanceTradeParser

def test_format_detector():
    file_path = Path("tests/csv_converter/sample_csv/kraken_v1.csv")

    reader = CSVReader()
    document = reader.read(file_path)
    detector = CSVFormatDetector()
    parser = detector.detect(document)

    assert isinstance(parser, KrakenTransactionParser)

def test_binance_detector():
    file_path = Path("tests/csv_converter/sample_csv/binance_trade.csv")


    reader = CSVReader()
    document = reader.read(file_path)
    detector = CSVFormatDetector()
    parser = detector.detect(document)

    assert isinstance(parser, BinanceTradeParser)

