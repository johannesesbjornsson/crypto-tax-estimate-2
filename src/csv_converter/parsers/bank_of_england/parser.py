from datetime import datetime
from decimal import Decimal
import re
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from csv_converter.reader.csv_document import CSVDocument
from domain.models.exchange_rate import ExchangeRate
from domain.models.source import Source



class BankOfEnglandUSDtoGBPParser:
    RATE_HEADER="Spot exchange rate, US $ into Sterling  						[a] [a] [a] 						XUDLUSS"
    REQUIRED_COLUMNS = {
        RATE_HEADER,
        "Date",
    }
    def can_parse(self, document: CSVDocument) -> bool:
        return self.REQUIRED_COLUMNS.issubset(
            set(document.headers)
        )
    
    def parse(self, document: CSVDocument) -> list[ExchangeRate]:
        rates = []
        for row in document.rows:
            rate = ExchangeRate(
                timestamp=datetime.strptime(
                    row["Date"],
                    "%d %b %y",
                ),
                source=Source(
                    venue="boe",
                    source_file=document.document_name
                ),
                from_currency="GBP",
                to_currency="USD",
                exchange_rate=Decimal(row[self.RATE_HEADER])
            )

            rates.append(rate)

        return rates
        