from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import (
    intpk,
    str_20,
    str_50,
    str_255,
    create_date,
    update_date,
)
from typing import List, TYPE_CHECKING
from sqlalchemy.ext.hybrid import hybrid_method

if TYPE_CHECKING:
    from .user_role import UserRole
    from .lookup.role import Role
    from .bid import Bid
    from .bid_manager import BidManager
    from .project_manager import ProjectManager
    from .comment import Comment


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column()
    username: Mapped[str_20] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str_255] = mapped_column()
    first_name: Mapped[str_50] = mapped_column()
    last_name: Mapped[str_50] = mapped_column()
    role_associations: Mapped[List["UserRole"]] = relationship(back_populates="user")
    roles: Mapped[List["Role"]] = relationship(
        secondary="user_role", back_populates="users", viewonly=True
    )
    bids: Mapped[List["Bid"]] = relationship(
        secondary="bid_manager", back_populates="bid_managers", viewonly=True
    )
    bid_associations: Mapped[List["BidManager"]] = relationship(
        back_populates="manager"
    )
    projects: Mapped[List["Bid"]] = relationship(
        secondary="project_manager", back_populates="project_managers", viewonly=True
    )
    project_associations: Mapped[List["ProjectManager"]] = relationship(
        back_populates="manager"
    )
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()

    @hybrid_method
    def has_role(self, role_name: str) -> bool:
        return any(role.name == role_name for role in self.roles)
