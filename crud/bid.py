from sqlalchemy.orm import Session
from schemas.bid import BidCreate, BidUpdate
from models.bid import Bid
from sqlalchemy import select
from models.bid_attribute import BidAttribute
from models.bid_estimate import BidEstimate
from fastapi.encoders import jsonable_encoder
from schemas.bid_estimate import BidEstimateUpdate


def create(db: Session, bid: BidCreate):
    new_bid = Bid(
        **bid.model_dump(exclude={"attributes": True, "estimated_data": True}),
        estimated_data=BidEstimate(**bid.estimated_data.model_dump(exclude_unset=True)),
        attributes=[
            BidAttribute(**attribute.model_dump(exclude_unset=True))
            for attribute in bid.attributes
        ],
    )
    db.add(new_bid)
    return new_bid


def update(db: Session, bid: Bid, update_in: BidUpdate):
    db_obj = jsonable_encoder(bid)
    update_obj = update_in.model_dump(exclude_unset=True)
    for field in db_obj:
        if field in update_obj:
            setattr(bid, field, update_obj[field])
    db.add(bid)
    return bid


def get_by_id(bid_id: int, db: Session):
    return db.scalars(select(Bid).where(Bid.id == bid_id)).first()


def update_estimates(
    db: Session, bid_estimates: BidEstimate, update_in: BidEstimateUpdate
):
    db_obj = jsonable_encoder(bid_estimates)
    update_obj = update_in.model_dump(exclude_unset=True)
    for field in db_obj:
        if field in update_obj:
            setattr(bid_estimates, field, update_obj[field])
    db.add(bid_estimates)
    return bid_estimates


def get(db: Session):
    return db.scalars(select(Bid)).all()
