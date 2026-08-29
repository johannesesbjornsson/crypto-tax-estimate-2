from pathlib import Path
from decimal import Decimal

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.parsers.bank_of_england.exchange_rate import BankOfEnglandUSDtoGBPParser
from domain.models.exchange_rate import ExchangeRate


def test_kraken_parser():
    file_path = Path("tests/csv_converter/sample_csv/boe_database.csv")

    reader = CSVReader()
    document = reader.read(file_path)

    parser = BankOfEnglandUSDtoGBPParser()

    exchange_rates = parser.parse(document)

    assert len(exchange_rates) == 7


    rates = [
        rate
        for rate in exchange_rates
        if isinstance(rate, ExchangeRate)
    ]

    assert len(rates) == 7

    rate_1 = rates[0]
    

    assert rate_1.to_currency == "USD"
    assert rate_1.from_currency == "GBP"
    assert rate_1.exchange_rate == Decimal('1.3582')

    rate_3 = rates[2]

    assert rate_3.from_currency == "GBP"
    assert rate_3.to_currency == "USD"
    assert rate_3.exchange_rate == Decimal('1.3633')
