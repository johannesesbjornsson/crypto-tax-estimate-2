from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from database.models.currency import CurrencyModel
from database.models.stablecoin import StablecoinModel


class ExchangeRateModel(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    from_currency_code: Mapped[str] = mapped_column(
        "from_currency",
        String(10),
        ForeignKey("currencies.code"),
        nullable=False,
    )

    to_currency_code: Mapped[str] = mapped_column(
        "to_currency",
        String(10),
        ForeignKey("currencies.code"),
        nullable=False,
    )

    rate: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
    )

    source: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    from_currency: Mapped["CurrencyModel"] = relationship(
        "CurrencyModel",
        foreign_keys=[from_currency_code],
    )

    to_currency: Mapped["CurrencyModel"] = relationship(
        "CurrencyModel",
        foreign_keys=[to_currency_code],
    )