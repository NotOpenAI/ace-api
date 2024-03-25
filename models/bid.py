from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.types import *
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy.ext.hybrid import hybrid_property


if TYPE_CHECKING:
    from .user import User
    from .customer import Customer
    from .bid_attribute import BidAttribute
    from .bid_manager import BidManager
    from .project_manager import ProjectManager


class Bid(Base):
    __tablename__ = "bid"
    id: Mapped[intpk] = mapped_column()
    name: Mapped[str_50] = mapped_column()
    bid_managers: Mapped[List["User"]] = relationship(
        secondary="bid_manager", back_populates="bids", viewonly=True
    )
    bm_associations: Mapped[List["BidManager"]] = relationship(back_populates="bid")
    project_managers: Mapped[List["User"]] = relationship(
        secondary="project_manager", back_populates="projects", viewonly=True
    )
    pm_associations: Mapped[List["ProjectManager"]] = relationship(
        back_populates="project"
    )
    lead: Mapped[Optional[str_100]] = mapped_column()
    foreman: Mapped[Optional[str_100]] = mapped_column()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="bids")
    start_date: Mapped[Optional[dt]] = mapped_column()
    finish_date: Mapped[Optional[dt]] = mapped_column()
    original_contract: Mapped[Optional[currency]] = mapped_column()
    original_cost: Mapped[Optional[currency]] = mapped_column()
    attributes: Mapped[List["BidAttribute"]] = relationship()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()

    @hybrid_property
    def margin(self) -> currency:
        if not self.original_cost or not self.original_contract:
            return currency(0)
        return 1 - (self.original_cost / self.original_contract)
