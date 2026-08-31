from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.models.currency import CurrencyModel


class StablecoinModel(Base):
    __tablename__ = "stablecoins"

    code: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    peg_currency_code: Mapped[str] = mapped_column(
        "peg_currency",
        String(10),
        ForeignKey("currencies.code"),
        nullable=False,
    )

    peg_ratio: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
        default=Decimal("1"),
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    peg_currency: Mapped["CurrencyModel"] = relationship(
        "CurrencyModel",
        back_populates="stablecoins",
    )