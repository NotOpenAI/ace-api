from db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column
from db.types import intpk, str_20


class Contract(Base):
    __tablename__ = "contract"

    id: Mapped[intpk] = mapped_column()
    name: Mapped[str_20] = mapped_column(unique=True)
    __table_args__ = {"schema": "lookup"}
