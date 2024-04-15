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
    from .lookup.job_status import JobStatus
    from .lookup.bid_status import BidStatus
    from .comment import Comment


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
    bid_status_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lookup.bid_status.id")
    )
    bid_status: Mapped["BidStatus"] = relationship(back_populates="bid")
    lead: Mapped[Optional[str_100]] = mapped_column()
    foreman: Mapped[Optional[str_100]] = mapped_column()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(back_populates="bids")
    job_status_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("lookup.job_status.id")
    )
    job_status: Mapped["JobStatus"] = relationship(back_populates="bid")
    comments: Mapped[List["Comment"]] = relationship(back_populates="bid")
    start_date: Mapped[Optional[dt]] = mapped_column()
    finish_date: Mapped[Optional[dt]] = mapped_column()
    original_contract: Mapped[Optional[currency]] = mapped_column()
    final_cost: Mapped[Optional[currency]] = mapped_column()
    desired_margin: Mapped[Optional[currency]] = mapped_column()
    attributes: Mapped[List["BidAttribute"]] = relationship()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()

    @hybrid_property
    def actual_margin(self) -> Optional[currency]:
        if not self.final_cost or not self.original_contract:
            return None
        return (1 - (self.final_cost / self.original_contract)).quantize(
            currency("1.00")
        )
