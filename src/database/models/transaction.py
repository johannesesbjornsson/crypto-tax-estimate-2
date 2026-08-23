from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.models.trade import TradeModel
    from database.models.income import IncomeModel
    from database.models.withdrawl import WithdrawlModel
    from database.models.deposit import DepositModel


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    venue: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_file: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    trade: Mapped["TradeModel | None"] = relationship(
        "TradeModel",
        back_populates="transaction",
        cascade="all, delete-orphan",
        uselist=False,
    )

    income: Mapped["IncomeModel | None"] = relationship(
        "IncomeModel",
        back_populates="transaction",
        cascade="all, delete-orphan",
        uselist=False,
    )

    withdrawl: Mapped["WithdrawlModel | None"] = relationship(
        "WithdrawlModel",
        back_populates="transaction",
        cascade="all, delete-orphan",
        uselist=False,
    )

    deposit: Mapped["DepositModel | None"] = relationship(
        "DepositModel",
        back_populates="transaction",
        cascade="all, delete-orphan",
        uselist=False,
    )