
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

from typing import TYPE_CHECKING

from database.models.wrapped_crypto_asset import WrappedCryptoAssetModel



class CryptoAssetModel(Base):
    __tablename__ = "crypto_assets"

    code: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    wrapped_crypto_assets: Mapped[list["WrappedCryptoAssetModel"]] = relationship(
        "WrappedCryptoAssetModel",
        back_populates="underlying_asset",
    )