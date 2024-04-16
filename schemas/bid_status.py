from schemas.base import GlobalBase


class BidStatusBase(GlobalBase):
    value: str


class BidStatusCreate(BidStatusBase):
    pass


class BidStatus(BidStatusBase):
    id: int

    class Config:
        from_attributes = True
