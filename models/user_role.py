from sqlalchemy import ForeignKey
from db.base_class import Base
from db.types import intpk, create_date, update_date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .lookup.role import Role
    from .user import User


class UserRole(Base):
    __tablename__ = "user_role"

    user_id: Mapped[intpk] = mapped_column(ForeignKey("user.id"))
    role_id: Mapped[intpk] = mapped_column(ForeignKey("lookup.role.id"))
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()
    role: Mapped["Role"] = relationship(back_populates="user_associations")
    user: Mapped["User"] = relationship(back_populates="role_associations")
