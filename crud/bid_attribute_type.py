from sqlalchemy.orm import Session, selectinload
from schemas.bid_attribute_type import BidAttributeTypeCreate, BidAttributeTypeUpdate
from models.lookup.bid_attribute_type import BidAttributeType
from sqlalchemy import select
from models.lookup.bid_attribute_option import BidAttributeOption
from fastapi.encoders import jsonable_encoder


def create(db: Session, bid_attribute_type: BidAttributeTypeCreate):
    new_bid_attribute_type = BidAttributeType(
        **bid_attribute_type.model_dump(exclude_unset=True, exclude={"options": True}),
        options=[
            BidAttributeOption(**option.model_dump(exclude_unset=True))
            for option in bid_attribute_type.options
        ],
    )
    db.add(new_bid_attribute_type)
    return new_bid_attribute_type


def update(
    db: Session, bid_attribute_type: BidAttributeType, update_in: BidAttributeTypeUpdate
):
    db_obj = jsonable_encoder(bid_attribute_type)
    update_obj = update_in.model_dump(exclude_unset=True, exclude={"options": True})
    for field in db_obj:
        if field in update_obj:
            setattr(bid_attribute_type, field, update_obj[field])
    db.add(bid_attribute_type)
    return bid_attribute_type


def get_by_id(db: Session, id: int):
    return db.scalars(
        select(BidAttributeType)
        .where(BidAttributeType.id == id)
        .options(
            selectinload(
                BidAttributeType.options.and_(BidAttributeOption.active == True)
            )
        )
        .execution_options(populate_existing=True)
    ).first()


def get_by_name(db: Session, name: str):
    return db.scalars(
        select(BidAttributeType)
        .where(BidAttributeType.name.ilike(name))
        .options(
            selectinload(
                BidAttributeType.options.and_(BidAttributeOption.active == True)
            )
        )
        .execution_options(populate_existing=True)
    ).first()


def get(db: Session):
    return db.scalars(select(BidAttributeType)).all()
