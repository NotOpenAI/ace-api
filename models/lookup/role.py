from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, str_20
from typing import List, TYPE_CHECKING


if TYPE_CHECKING:
    from ..user_role import UserRole


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk] = mapped_column()
    name: Mapped[str_20] = mapped_column(unique=True)
    users: Mapped[List["UserRole"]] = relationship(back_populates="role")
    __table_args__ = {"schema": "lookup"}
