from sqlalchemy import ForeignKey
from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from db.types import intpk, create_date, update_date, str_50


class AttributeOption(Base):
    __tablename__ = "attribute_option"

    id: Mapped[intpk] = mapped_column()
    attribute_id: Mapped[int] = mapped_column(ForeignKey("lookup.attribute.id"))
    name: Mapped[str_50] = mapped_column()
    created_at: Mapped[create_date] = mapped_column()
    updated_at: Mapped[update_date] = mapped_column()
