from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from database.models.crypto_asset import CryptoAssetModel
from database.models.stablecoin import StablecoinModel
from database.models.currency import CurrencyModel


class MarketPriceModel(Base):
    __tablename__ = "market_prices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    asset_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("crypto_assets.code"),
        nullable=False,
    )

    quote_currency_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("stablecoins.code"),
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

    asset: Mapped["CryptoAssetModel"] = relationship(
        "CryptoAssetModel",
    )

    quote_currency: Mapped["StablecoinModel"] = relationship(
        "StablecoinModel",
    )