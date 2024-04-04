from sqlalchemy.orm import Session
from schemas.bid import BidCreate, BidUpdate
from models.bid import Bid
from models.bid_manager import BidManager
from models.project_manager import ProjectManager
from sqlalchemy import select, delete
from models.bid_attribute import BidAttribute
from fastapi.encoders import jsonable_encoder
from typing import Optional, List


def create(db: Session, bid: BidCreate):
    new_bid = Bid(
        **bid.model_dump(exclude={"attributes": True, "bid_manager_ids": True}),
        attributes=[
            BidAttribute(**attribute.model_dump(exclude_unset=True))
            for attribute in bid.attributes
        ],
        bm_associations=[BidManager(manager_id=id) for id in bid.bid_manager_ids]
    )
    db.add(new_bid)
    return new_bid


def update(db: Session, bid: Bid, update_in: BidUpdate):
    db_obj = jsonable_encoder(bid)
    update_obj = update_in.model_dump(exclude_unset=True)

    if update_in.bid_manager_ids:
        db.execute(delete(BidManager).where(BidManager.bid_id == bid.id))
        setattr(
            bid,
            "bm_associations",
            [BidManager(manager_id=id) for id in update_in.bid_manager_ids],
        )

    if update_in.project_manager_ids:
        db.execute(delete(ProjectManager).where(ProjectManager.project_id == bid.id))
        setattr(
            bid,
            "pm_associations",
            [ProjectManager(manager_id=id) for id in update_in.project_manager_ids],
        )

    for field in db_obj:
        if field in update_obj:
            setattr(bid, field, update_obj[field])
    db.add(bid)
    return bid


def get_by_id(bid_id: int, db: Session):
    return db.scalars(select(Bid).where(Bid.id == bid_id)).first()


def get(
    db: Session,
    customer_id: Optional[int] = None,
    bid_manager_ids: Optional[List[int]] = None,
):
    query = select(Bid)
    if customer_id:
        query = query.where(Bid.customer_id == customer_id)
    if bid_manager_ids:
        query = query.where(Bid.bid_managers.in_(bid_manager_ids))
    return db.scalars(query).all()
