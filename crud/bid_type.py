from sqlalchemy.orm import Session
from schemas.bid_type import BidTypeCreate
from models.lookup.bid_type import BidType
from sqlalchemy import select


def create(db: Session, bid_type: BidTypeCreate):
    new_bid_type = BidType(**bid_type.model_dump())
    db.add(new_bid_type)
    return new_bid_type


def get(db: Session):
    return db.scalars(select(BidType)).all()
