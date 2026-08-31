# database/models/crypto_asset.py

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


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