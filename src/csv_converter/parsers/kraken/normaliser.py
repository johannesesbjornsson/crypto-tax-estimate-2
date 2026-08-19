from domain.models.transaction import Transaction, Income, Trade, TransactionSource
from .transaction import KrakenTransaction, KrakenTrade, KrakenStaking, KrakenDeposit, KrakenWithdrawl

class Krakennormaliser:

    def normalize(self, transaction: KrakenTransaction) -> Transaction:

        if isinstance(transaction, KrakenTrade):
            return self.normalize_trade(transaction)

        if isinstance(transaction, KrakenDeposit):
            return

        if isinstance(transaction, KrakenWithdrawl):
            return

        if isinstance(transaction, KrakenStaking):
            return self.normalize_staking(transaction)

        raise ValueError(
            f"Unsupported Kraken transaction: "
            f"{type(transaction).__name__}"
        )

    def normalize_trade(self, trade: KrakenTrade) -> Trade:
        print(trade)
        return Trade(
            id=trade.tx_id,
            timestamp=trade.timestamp,
            from_asset=trade.from_asset,
            from_asset_amount=trade.from_asset_amount,
            to_asset=trade.to_asset,
            to_asset_amount=trade.to_asset_amount,
            fee_asset=trade.fee_asset,
            fee_amount=trade.fee,
            exchange_rate=trade.price,
            source=TransactionSource(
                venue="kraken",
                source_file=trade.source
            ),
        )
    def normalize_staking(self, staking: KrakenStaking) -> Income:
        return Income(
            id=staking.tx_id,
            timestamp=staking.timestamp,
            asset=staking.asset,
            amount=staking.amount,
            source=TransactionSource(
                venue="kraken",
                source_file=None
            ),
        )
