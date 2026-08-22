from pathlib import Path
from decimal import Decimal

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.parsers.binance.trade import BinanceTradeParser
from domain.models.transaction import Trade, Income


def test_kraken_parser():
    file_path = Path("tests/csv_converter/sample_csv/binance_trade.csv")

    reader = CSVReader()
    document = reader.read(file_path)

    parser = BinanceTradeParser()

    transactions = parser.parse(document)

    assert len(transactions) == 4


    trades = [
        transaction
        for transaction in transactions
        if isinstance(transaction, Trade)
    ]

    assert len(trades) == 4

    trade_1 = trades[0]
    

    assert trade_1.to_asset == "SOL"
    assert trade_1.from_asset == "USDT"
    assert trade_1.exchange_rate == Decimal('72.3500000000') 
    assert trade_1.fee_amount == Decimal('0.0001846500')
    assert trade_1.fee_asset == "BNB"

    trade_3 = trades[2]

    assert trade_3.to_asset == "USDT"
    assert trade_3.from_asset == "EGLD"
    assert trade_3.exchange_rate == Decimal('0.01664170411050091529372607755') 
