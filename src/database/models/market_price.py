from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base



class MarketPriceModel(Base):
    __tablename__ = "market_prices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    asset: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    quote_currency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    interval: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
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