from datetime import datetime, timezone
from decimal import Decimal

from csv_converter.reader.csv_document import CSVDocument
from csv_converter.parsers.binance_klines.models import BinanceKline
from domain.models.exchange_rate import MarketPrice
from .normaliser import BinanceKlineNormaliser

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
        return self.REQUIRED_COLUMNS.issubset(
            set(document.headers)
        )

    def _parse_binance_kline(self, row: map, file_name: str, asset:str, quote_currency:str) -> BinanceKline:
        # Binance changed timestamp precision
        if int(row["open time"]) >= 1_000_000_000_000_000:
            open_timestamp=int(row["open time"]) / 1_000_000
            close_timestamp=int(row['close time']) / 1_000_000
        else:
            open_timestamp=int(row["open time"]) / 1_000
            close_timestamp=int(row['close time']) / 1_000

        kline = BinanceKline(
            open_time = datetime.fromtimestamp(
                open_timestamp,
                tz=timezone.utc,
            ),
            open=Decimal(row['open']),
            high=Decimal(row['high']),
            low=Decimal(row['low']),
            close=Decimal(row['close']),
            volume=Decimal(row['volume']),
            close_time= datetime.fromtimestamp(
                close_timestamp,
                tz=timezone.utc,
            ),
            quote_asset_volume=Decimal(row['quote asset volume']),
            number_of_trades=int(row['number of trades']),
            taker_buy_base_asset_volume=Decimal(row['taker buy base asset volume']),
            taker_buy_quote_asset_volume=Decimal(row['taker buy quote asset volume']),
            source_file=file_name,
            asset=asset,
            quote_currency=quote_currency
        )
        return kline

    def parse_candles(self, document: CSVDocument, asset:str, quote_currency:str) -> list[BinanceKline]:
        klines = []
        for row in document.rows:
            kline = self._parse_binance_kline(
                row=row,
                file_name=document.document_name,
                asset=asset,
                quote_currency=quote_currency
                )
            klines.append(kline)

        return klines

    def parse(self, document: CSVDocument, asset:str, quote_currency:str) -> list[MarketPrice]:
        klines = []
        normaliser = BinanceKlineNormaliser()
        for row in document.rows:
            kline = self._parse_binance_kline(
                row=row,
                file_name=document.document_name,
                asset=asset,
                quote_currency=quote_currency
                )
            klines.append(normaliser.normalise(kline))

        return klines

