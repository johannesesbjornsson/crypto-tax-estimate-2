from sqlalchemy.orm import Session

from domain.models.transaction import Trade, Income, Deposit, Withdrawl

from database.models.transaction import TransactionModel
from database.models.trade import TradeModel
from database.models.income import IncomeModel
from database.models.deposit import DepositModel
from database.models.withdrawl import WithdrawlModel


class TransactionRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, transaction):
        if isinstance(transaction, Trade):
            self._save_trade(transaction)

        elif isinstance(transaction, Income):
            self._save_income(transaction)

        elif isinstance(transaction, Deposit):
            self._save_deposit(transaction)

        elif isinstance(transaction, Withdrawl):
            self._save_withdrawl(transaction)

        else:
            raise ValueError(
                f"Unsupported transaction type: "
                f"{type(transaction).__name__}"
            )

    def _save_trade(self, trade: Trade):

        transaction = TransactionModel(
            checksum=trade.checksum,
            venue_txn_id=trade.venue_txn_id,
            timestamp=trade.timestamp,
            venue=trade.source.venue,
            source_file=trade.source.source_file,
        )

        TradeModel(
            from_asset=trade.from_asset,
            from_asset_amount=trade.from_asset_amount,
            to_asset=trade.to_asset,
            to_asset_amount=trade.to_asset_amount,
            fee_asset=trade.fee_asset,
            fee_amount=trade.fee_amount,
            exchange_rate=trade.exchange_rate,
            transaction=transaction,
        )

        self.session.add(transaction)

    def _save_income(self, income: Income):

        transaction = TransactionModel(
            checksum=income.checksum,
            venue_txn_id=income.venue_txn_id,
            timestamp=income.timestamp,
            venue=income.source.venue,
            source_file=income.source.source_file,
        )

        IncomeModel(
            asset=income.asset,
            amount=income.amount,
            transaction=transaction,
        )

        self.session.add(transaction)

    def _save_deposit(self, deposit: Deposit):

        transaction = TransactionModel(
            checksum=deposit.checksum,
            venue_txn_id=deposit.venue_txn_id,
            timestamp=deposit.timestamp,
            venue=deposit.source.venue,
            source_file=deposit.source.source_file,
        )

        DepositModel(
            asset=deposit.asset,
            amount=deposit.amount,
            transaction=transaction,
        )

        self.session.add(transaction)

    def _save_withdrawl(self, withdrawl: Withdrawl):

        transaction = TransactionModel(
            checksum=withdrawl.checksum,
            venue_txn_id=withdrawl.venue_txn_id,
            timestamp=withdrawl.timestamp,
            venue=withdrawl.source.venue,
            source_file=withdrawl.source.source_file,
        )

        WithdrawlModel(
            asset=withdrawl.asset,
            amount=withdrawl.amount,
            transaction=transaction,
        )

        self.session.add(transaction)

    def commit(self):
        self.session.commit()

