from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.models.crypto_asset import CryptoAssetModel

class WrappedCryptoAssetModel(Base):
    __tablename__ = "wrapped_crypto_assets"

    code: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    underlying_asset_code: Mapped[str] = mapped_column(
        "underlying_asset",
        String(10),
        ForeignKey("crypto_assets.code"),
        nullable=False,
    )

    underlying_asset: Mapped["CryptoAssetModel"] = relationship(
        "CryptoAssetModel",
        back_populates="wrapped_crypto_assets",
    )