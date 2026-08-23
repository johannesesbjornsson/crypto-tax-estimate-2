from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.models.transaction import TransactionModel


class DepositModel(Base):
    __tablename__ = "deposit"

    id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    asset: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
    )

    transaction: Mapped["TransactionModel"] = relationship(
        "TransactionModel",
        back_populates="deposit",
    )