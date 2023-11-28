from sqlalchemy.orm import Session
from schemas.bid_attribute import BidAttributeCreateDB, BidAttributeUpdate
from models.bid_attribute import BidAttribute
from sqlalchemy import select, delete
from fastapi.encoders import jsonable_encoder


def create(db: Session, bid_attribute: BidAttributeCreateDB):
    new_bid_attribute = BidAttribute(**bid_attribute.model_dump(exclude_unset=True))
    db.add(new_bid_attribute)
    return new_bid_attribute


def update(db: Session, bid_attribute: BidAttribute, update_in: BidAttributeUpdate):
    db_obj = jsonable_encoder(bid_attribute)
    update_obj = update_in.model_dump(exclude_unset=True, exclude={"id": True})
    for field in db_obj:
        if field in update_obj:
            setattr(bid_attribute, field, update_obj[field])
    db.add(bid_attribute)
    return bid_attribute


def bulk_remove(db: Session, bid_attribute_ids: set[int]):
    db.execute(delete(BidAttribute).where(BidAttribute.id.in_(bid_attribute_ids)))


def get_by_bid_type_id(db: Session, bid_id: int, type_id: int):
    return db.scalars(
        select(BidAttribute).where(
            (BidAttribute.bid_id == bid_id) & (BidAttribute.type_id == type_id)
        )
    ).first()
