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
from typing import Set, TYPE_CHECKING


if TYPE_CHECKING:
    from .user_role import UserRole


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column()
    username: Mapped[str_20] = mapped_column(unique=True, index=True)
    password: Mapped[str_255] = mapped_column()
    first_name: Mapped[str_50] = mapped_column()
    last_name: Mapped[str_50] = mapped_column()
    roles: Mapped[Set["UserRole"]] = relationship(back_populates="user")
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()
