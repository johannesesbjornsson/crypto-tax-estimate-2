from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.models.transaction import TransactionModel


class TradeModel(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    from_asset: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    from_asset_amount: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
    )

    to_asset: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    to_asset_amount: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
    )

    fee_asset: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    fee_amount: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
    )

    exchange_rate: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
    )

    transaction: Mapped["TransactionModel"] = relationship(
        "TransactionModel",
        back_populates="trade",
    )