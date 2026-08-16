from datetime import datetime
from decimal import Decimal
import re 

from csv_converter.reader.csv_document import CSVDocument
from csv_converter.parsers.binance.models import (
    BinanceTrade,
)


class BinanceTradeParser:

    REQUIRED_COLUMNS = {
        "Date(UTC)",
        "Pair",
        "Side",
        "Price",
        "Executed",
        "Amount",
        "Fee",
    }

    def can_parse(self, document: CSVDocument) -> bool:
        return self.REQUIRED_COLUMNS.issubset(
            set(document.headers)
        )

    def parse_amount_asset_string(self, asset_string: str) -> tuple[Decimal, str]:
        m = re.search('([0-9\.]+)([A-Z]+)', asset_string)
        if m:
            return Decimal(m.group(1)), m.group(2)
        else:
            raise ValueError(f"Unable to find both amount and currency in string {asset_string}")



    def parse(self, document: CSVDocument) -> list[BinanceTrade]:
        trades = []

        for row in document.rows:
            fee, fee_assset = self.parse_amount_asset_string(row["Fee"])
            base_currency, base_currency_amount = self.parse_amount_asset_string(row["Executed"])
            quote_currency, quote_currency_amount = self.parse_amount_asset_string(row["Amount"])

            trade = BinanceTrade(
                timestamp=datetime.strptime(
                    row["Date(UTC)"],
                    "%Y-%m-%d %H:%M:%S",
                ),
                pair=row["Pair"],
                side=row["Side"],
                price=Decimal(row["Price"]),
                base_currency=base_currency,
                base_currency_amount=base_currency_amount,
                quote_currency=quote_currency,
                quote_currency_amount=quote_currency_amount,
                fee=fee,
                fee_asset=fee_assset,
            )

            trades.append(trade)

        return trades

