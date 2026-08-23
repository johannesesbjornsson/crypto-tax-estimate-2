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
            id=trade.id,
            timestamp=trade.timestamp,
            venue=trade.source.venue,
            source_file=trade.source.source_file,
        )

        trade_model = TradeModel(
            id=trade.id,
            from_asset=trade.from_asset,
            from_asset_amount=trade.from_asset_amount,
            to_asset=trade.to_asset,
            to_asset_amount=trade.to_asset_amount,
            fee_asset=trade.fee_asset,
            fee_amount=trade.fee_amount,
            exchange_rate=trade.exchange_rate,
        )

        self.session.add(transaction)
        self.session.add(trade_model)

    def _save_income(self, income: Income):

        transaction = TransactionModel(
            id=income.id,
            timestamp=income.timestamp,
            venue=income.source.venue,
            source_file=income.source.source_file,
        )

        income_model = IncomeModel(
            id=income.id,
            asset=income.asset,
            amount=income.amount,
        )

        self.session.add(transaction)
        self.session.add(income_model)

    def _save_withdrawl(self, withdrawl: Withdrawl):

        transaction = TransactionModel(
            id=withdrawl.id,
            timestamp=withdrawl.timestamp,
            venue=withdrawl.source.venue,
            source_file=withdrawl.source.source_file,
        )

        withdrawl_model = WithdrawlModel(
            id=withdrawl.id,
            asset=withdrawl.asset,
            amount=withdrawl.amount,
        )

        self.session.add(transaction)
        self.session.add(withdrawl_model)

    def _save_deposit(self, deposit: Deposit):

        transaction = TransactionModel(
            id=deposit.id,
            timestamp=deposit.timestamp,
            venue=deposit.source.venue,
            source_file=deposit.source.source_file,
        )

        deposit_model = DepositModel(
            id=deposit.id,
            asset=deposit.asset,
            amount=deposit.amount,
        )

        self.session.add(transaction)
        self.session.add(deposit_model)

    def commit(self):
        self.session.commit()