from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bid import Bid
    from .user import User


class ProjectManager(Base):
    __tablename__ = "project_manager"
    manager_id: Mapped[intpk] = mapped_column(ForeignKey("user.id"))
    project_id: Mapped[intpk] = mapped_column(ForeignKey("bid.id"))
    project: Mapped["Bid"] = relationship(back_populates="pm_associations")
    manager: Mapped["User"] = relationship(back_populates="project_associations")
