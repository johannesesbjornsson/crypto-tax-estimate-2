from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base



class ExchangeRateModel(Base):
    __tablename__ = "exchange_rates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    from_currency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    to_currency: Mapped[str] = mapped_column(
        String(20),
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