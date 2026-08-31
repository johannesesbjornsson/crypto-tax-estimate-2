from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from database.models.stablecoin import StablecoinModel

class CurrencyModel(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    stablecoins: Mapped[list["StablecoinModel"]] = relationship(
        "StablecoinModel",
        back_populates="peg_currency",
    )