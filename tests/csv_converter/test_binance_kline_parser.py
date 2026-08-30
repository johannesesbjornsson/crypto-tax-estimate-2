from datetime import datetime
from pathlib import Path
from decimal import Decimal

from csv_converter.reader.csv_reader import CSVReader
from csv_converter.parsers.binance_klines.parser import BinanceKlineParser
from domain.models.exchange_rate import MarketPrice


def test_binance_kline_parser_2022():
    file_path = Path("tests/csv_converter/sample_csv/binance_klines_2022.csv")

    reader = CSVReader()
    document = reader.read(file_path)

    parser = BinanceKlineParser()

    exchange_rates = parser.parse(document,asset="BTC",quote_currency="USDT")

    assert len(exchange_rates) == 6


    market_prices = [
        rate
        for rate in exchange_rates
        if isinstance(rate, MarketPrice)
    ]

    assert len(market_prices) == 6

    market_price_1 = market_prices[0]
    

    assert market_price_1.asset == "BTC"
    assert market_price_1.quote_currency == "USDT"
    assert market_price_1.price == Decimal('43160.00000000') 
    assert market_price_1.timestamp == datetime.fromisoformat(
        "2022-03-01T00:00:00+00:00"
    )
    assert market_price_1.interval == "1h"

    market_price_4 = market_prices[3]

    assert market_price_4.asset == "BTC"
    assert market_price_4.quote_currency == "USDT"
    assert market_price_4.price == Decimal('43160.01000000') 
    assert market_price_4.timestamp == datetime.fromisoformat(
        "2022-03-01T03:00:00+00:00"
    )



def test_binance_kline_parser_2025():
    file_path = Path("tests/csv_converter/sample_csv/binance_klines_2025.csv")

    reader = CSVReader()
    document = reader.read(file_path)

    parser = BinanceKlineParser()

    exchange_rates = parser.parse(document,asset="BTC",quote_currency="USDT")

    assert len(exchange_rates) == 3


    market_prices = [
        rate
        for rate in exchange_rates
        if isinstance(rate, MarketPrice)
    ]

    assert len(market_prices) == 3

    market_price_1 = market_prices[0]
    

    assert market_price_1.asset == "BTC"
    assert market_price_1.quote_currency == "USDT"
    assert market_price_1.price == Decimal('108246.36000000') 
    assert market_price_1.timestamp == datetime.fromisoformat(
        "2025-09-01T00:00:00+00:00"
    )
    assert market_price_1.interval == "1h"

    market_price_3 = market_prices[2]

    assert market_price_3.asset == "BTC"
    assert market_price_3.quote_currency == "USDT"
    assert market_price_3.price == Decimal('108150.24000000') 
    assert market_price_3.timestamp == datetime.fromisoformat(
        "2025-09-01T02:00:00+00:00"
    )



def test_binance_kline_parser_2025_raw_content():
    file_conent = """
1756684800000000,108246.36000000,108406.18000000,107631.68000000,108222.37000000,1078.82210000,1756688399999999,116502666.71286960,213874,478.02672000,51613477.68853730,0
1756688400000000,108222.37000000,108482.98000000,107968.09000000,108150.24000000,471.21562000,1756691999999999,50978640.87134690,168219,214.66579000,23223696.50407150,0
1756692000000000,108150.24000000,108197.67000000,107425.42000000,107617.05000000,869.81682000,1756695599999999,93716741.62590400,181538,352.16529000,37933955.71463300,0
"""

    reader = CSVReader()
    document = reader.read_content(
        content=file_conent, 
        document_name="test",
        custom_headers=["open time", "open", "high", "low", "close", "volume", "close time", "quote asset volume", "number of trades", "taker buy base asset volume", "taker buy quote asset volume", "ignore"]
    )

    parser = BinanceKlineParser()

    exchange_rates = parser.parse(document,asset="BTC",quote_currency="USDT")

    assert len(exchange_rates) == 3


    market_prices = [
        rate
        for rate in exchange_rates
        if isinstance(rate, MarketPrice)
    ]

    assert len(market_prices) == 3

    market_price_1 = market_prices[0]
    

    assert market_price_1.asset == "BTC"
    assert market_price_1.quote_currency == "USDT"
    assert market_price_1.price == Decimal('108246.36000000') 
    assert market_price_1.timestamp == datetime.fromisoformat(
        "2025-09-01T00:00:00+00:00"
    )
    assert market_price_1.interval == "1h"

    market_price_3 = market_prices[2]

    assert market_price_3.asset == "BTC"
    assert market_price_3.quote_currency == "USDT"
    assert market_price_3.price == Decimal('108150.24000000') 
    assert market_price_3.timestamp == datetime.fromisoformat(
        "2025-09-01T02:00:00+00:00"
    )