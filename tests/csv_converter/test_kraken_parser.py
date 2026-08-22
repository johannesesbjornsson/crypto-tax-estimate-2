from pathlib import Path
from decimal import Decimal

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.parsers.kraken.transaction import KrakenTransactionParser
from domain.models.transaction import Trade, Income


def test_kraken_parser():
    file_path = Path("tests/csv_converter/sample_csv/kraken_v1.csv")

    reader = CSVReader()
    document = reader.read(file_path)

    parser = KrakenTransactionParser()

    transactions = parser.parse(document)

    assert len(transactions) == 22


    trades = [
        transaction
        for transaction in transactions
        if isinstance(transaction, Trade)
    ]

    incomes = [
        transaction
        for transaction in transactions
        if isinstance(transaction, Income)
    ]


    assert len(trades) == 3
    assert len(incomes) == 18

    trade_1 = trades[0]
    

    assert trade_1.to_asset == "ETH"
    assert trade_1.from_asset == "GBP"
    assert trade_1.exchange_rate == Decimal('1276.849885800490043353560661')
    assert trade_1.fee_asset == "GBP"
    assert trade_1.fee_amount ==Decimal('0.2860')


    income_1 = incomes[0]

    assert income_1.asset == "MATIC"
    assert income_1.amount == Decimal('0.0800779900')