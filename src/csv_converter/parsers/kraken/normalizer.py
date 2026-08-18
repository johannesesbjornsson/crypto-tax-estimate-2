from domain.models.transaction import Transaction, Income, Trade, TransactionSource
from .transaction import KrakenTransaction, KrakenTrade, KrakenStaking, KrakenDeposit, KrakenWithdrawl

class KrakenNormalizer:

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
        return Trade(
            id=trade.tx_id,
            timestamp=trade.timestamp,
            from_asset=trade.quote_currency,
            from_amount=trade.quote_currency_amount,
            to_asset=trade.base_currency,
            to_amount=trade.base_currency_amount,
            fee_asset=trade.fee_asset,
            fee_amount=trade.fee,
            source=TransactionSource(
                venue="kraken",
                source_file=None
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
