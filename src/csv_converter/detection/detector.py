from typing import Protocol
import logging
logger = logging.getLogger(__name__)

from csv_converter.reader.csv_document import CSVDocument
from csv_converter.parsers.binance.trade import BinanceTradeParser
from csv_converter.parsers.kraken.transaction import KrakenTransactionParser

class CSVParser(Protocol):

    def can_parse(self, document: CSVDocument) -> bool:
        ...


class CSVFormatDetector:

    def __init__(self):
        self.parsers = [
            BinanceTradeParser(),
            KrakenTransactionParser()
        ]

    def detect(self, document: CSVDocument) -> CSVParser:

        matches = [
            parser
            for parser in self.parsers
            if parser.can_parse(document)
        ]

        if not matches:
            raise ValueError("Unknown CSV format")

        if len(matches) > 1:
            raise ValueError("Ambiguous CSV format")

        
        logger.info(f"Detected format {matches[0]}")
        
        return matches[0]