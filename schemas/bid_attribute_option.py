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


class BidAttributeOptionBulkUpdate(GlobalBase):
    update_options: Optional[list[BidAttributeOptionUpdate]] = None
    delete_options: Optional[set[int]] = None


class BidAttributeOption(BidAttributeOptionBase):
    id: int

    class Config:
        from_attributes = True


class BidAttributeOptionFull(BidAttributeOptionBase):
    id: int
    active: bool

    class Config:
        from_attributes = True
