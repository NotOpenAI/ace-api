from schemas.base import GlobalBase
from typing import Optional


class BidAttributeOptionBase(GlobalBase):
    value: str


class BidAttributeOptionCreate(BidAttributeOptionBase):
    pass


class BidAttributeOptionCreateDB(BidAttributeOptionCreate):
    attribute_type_id: int


class BidAttributeOptionUpdate(BidAttributeOptionBase):
    id: Optional[int] = None
    active: bool = True
    value: str


class BidAttributeOption(BidAttributeOptionBase):
    id: int

    class Config:
        from_attributes = True


class BidAttributeOptionFull(BidAttributeOptionBase):
    id: int
    active: bool

    class Config:
        from_attributes = True
