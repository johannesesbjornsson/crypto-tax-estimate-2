from csv_converter.parsers.binance.models import BinanceTrade
from decimal import Decimal
from domain.models.transaction import Transaction, TransactionSource, Trade

class BinanceTradenormaliser:



    def normalise(self, trade: BinanceTrade) -> Transaction:
        if trade.side == "BUY":
            from_asset = trade.quote_currency
            from_asset_amount = trade.quote_currency_amount
            to_asset = trade.base_currency
            to_asset_amount = trade.base_currency_amount
            exchange_rate = trade.price

        elif trade.side == "SELL":
            from_asset = trade.base_currency
            from_asset_amount = trade.base_currency_amount
            to_asset = trade.quote_currency
            to_asset_amount = trade.quote_currency_amount
            exchange_rate =  Decimal(from_asset_amount/to_asset_amount)
        else:
            raise ValueError(f"Invalid side {trade.side}")

        fee_asset = trade.fee_asset
        fee_amount = trade.fee

        return Trade(
            id=f"{trade.timestamp}-{trade.pair}-{trade.base_currency_amount}-{trade.quote_currency_amount}-{trade.price}",
            timestamp=trade.timestamp,
            from_asset=from_asset,
            from_asset_amount=from_asset_amount,
            to_asset=to_asset,
            to_asset_amount=to_asset_amount,
            fee_asset=fee_asset,
            fee_amount=fee_amount,
            exchange_rate=exchange_rate,
            source=TransactionSource(
                venue="binance",
                source_file=trade.source
            ),
        )

