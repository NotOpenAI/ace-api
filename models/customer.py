from sqlalchemy import Integer
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import (
    intpk,
    str_50,
    str_100,
    create_date,
    update_date,
)
from typing import List, TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from .bid import Bid
    from .customer_contact import CustomerContact


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[intpk] = mapped_column()
    name: Mapped[str_100] = mapped_column(unique=True, index=True)
    owner: Mapped[Optional[str_100]] = mapped_column()
    market: Mapped[Optional[str_50]] = mapped_column()
    reputation: Mapped[Optional[int]] = mapped_column(Integer)
    fin_health: Mapped[Optional[int]] = mapped_column(Integer)
    bids: Mapped[List["Bid"]] = relationship(back_populates="customer")
    contacts: Mapped[List["CustomerContact"]] = relationship(back_populates="customer")
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()
