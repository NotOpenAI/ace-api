from sqlalchemy import ForeignKey
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, create_date, update_date, str_100, str_50, str_20
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .customer import Customer


class CustomerContact(Base):
    __tablename__ = "customer_contact"

    id: Mapped[intpk] = mapped_column()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="contacts")
    name: Mapped[str_50] = mapped_column()
    email: Mapped[str_100] = mapped_column()
    phone: Mapped[str_20] = mapped_column()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()
