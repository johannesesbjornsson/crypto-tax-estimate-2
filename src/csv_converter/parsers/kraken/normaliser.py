from domain.models.transaction import Transaction, Income, Trade, TransactionSource, Withdrawl, Deposit
from .transaction import KrakenTransaction, KrakenTrade, KrakenStaking, KrakenDeposit, KrakenWithdrawl

class Krakennormaliser:

    def normalise(self, transaction: KrakenTransaction) -> Transaction:

        if isinstance(transaction, KrakenTrade):
            return self.normalise_trade(transaction)

        if isinstance(transaction, KrakenDeposit):
            return self.normalise_deposit(transaction)

        if isinstance(transaction, KrakenWithdrawl):
            return self.normalise_withdrawl(transaction)

        if isinstance(transaction, KrakenStaking):
            return self.normalise_staking(transaction)

        raise ValueError(
            f"Unsupported Kraken transaction: "
            f"{type(transaction).__name__}"
        )


    def normalise_withdrawl(self, withdrawl: KrakenWithdrawl) -> Withdrawl:
        return Withdrawl(
            id=withdrawl.tx_id,
            timestamp=withdrawl.timestamp,   
            asset=withdrawl.asset,
            amount=withdrawl.amount,
            source=TransactionSource(
                venue="kraken",
                source_file=withdrawl.source
            ), 
        )

    def normalise_deposit(self, deposit: KrakenDeposit) -> Deposit:
        return Deposit(
            id=deposit.tx_id,
            timestamp=deposit.timestamp,   
            asset=deposit.asset,
            amount=deposit.amount,
            source=TransactionSource(
                venue="kraken",
                source_file=deposit.source
            ), 
        )
    def normalise_trade(self, trade: KrakenTrade) -> Trade:
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
    def normalise_staking(self, staking: KrakenStaking) -> Income:
        return Income(
            id=staking.tx_id,
            timestamp=staking.timestamp,
            asset=staking.asset,
            amount=staking.amount,
            source=TransactionSource(
                venue="kraken",
                source_file=staking.source
            ),
        )
