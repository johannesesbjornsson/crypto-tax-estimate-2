from datetime import datetime, timezone
from decimal import Decimal

from csv_converter.reader.csv_document import CSVDocument
from csv_converter.parsers.binance_klines.models import BinanceKline

class BinanceKlineParser:
    REQUIRED_COLUMNS = {
        "open time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close time",
        "quote asset volume",
        "number of trades",
        "taker buy base asset volume",
        "taker buy quote asset volume",
        "ignore",
    }
    def can_parse(self, document: CSVDocument) -> bool:
        print(self.REQUIRED_COLUMNS)
        print(document.headers)
        return self.REQUIRED_COLUMNS.issubset(
            set(document.headers)
        )

    def _parse_binance_kline(self, row: map) -> BinanceKline:
        kline = BinanceKline(
            open_time = datetime.fromtimestamp(
                int(row["open time"]) / 1000,
                tz=timezone.utc,
            ),
            open=Decimal(row['open']),
            high=Decimal(row['high']),
            low=Decimal(row['low']),
            close=Decimal(row['close']),
            volume=Decimal(row['volume']),
            close_time= datetime.fromtimestamp(
                int(row['close time']) / 1000,
                tz=timezone.utc,
            ),
            quote_asset_volume=Decimal(row['quote asset volume']),
            number_of_trades=int(row['number of trades']),
            taker_buy_base_asset_volume=Decimal(row['taker buy base asset volume']),
            taker_buy_quote_asset_volume=Decimal(row['taker buy quote asset volume']),
        )
        return kline

    def parse_candles(self, document: CSVDocument) -> list[BinanceKline]:
        pass

    def parse(self, document: CSVDocument) -> list[BinanceKline]:
        klines = []
        for row in document.rows:
            kline = self._parse_binance_kline(row)
            klines.append(kline)

        return klines

