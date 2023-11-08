from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.types import intpk, str_20
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .attribute_type import AttributeType
    from .attribute_option import AttributeOption


class Attribute(Base):
    __tablename__ = "attribute"

    id: Mapped[intpk] = mapped_column()
    name: Mapped[str_20] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(server_default="1")
    required: Mapped[bool] = mapped_column(server_default="0")
    attribute_type_id: Mapped[int] = mapped_column(
        ForeignKey("lookup.attribute_type.id")
    )
    attribute_type: Mapped["AttributeType"] = relationship()
    options: Mapped[List["AttributeOption"]] = relationship()
    __table_args__ = {"schema": "lookup"}
