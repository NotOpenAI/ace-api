from sqlalchemy.orm import Session, selectinload
from schemas.bid_attribute_option import (
    BidAttributeOptionCreateDB,
    BidAttributeOptionUpdate,
)
from models.lookup.bid_attribute_type import BidAttributeType
from sqlalchemy import select, update as saupdate
from models.lookup.bid_attribute_option import BidAttributeOption
from fastapi.encoders import jsonable_encoder


def create(db: Session, bid_attribute_type: BidAttributeOptionCreateDB):
    new_bid_attribute_option = BidAttributeOption(
        **bid_attribute_type.model_dump(exclude_none=True),
    )
    db.add(new_bid_attribute_option)
    return new_bid_attribute_option


def bulk_delete(db: Session, option_ids: set[int]):
    db.execute(
        saupdate(BidAttributeOption)
        .where(BidAttributeOption.id.in_(option_ids))
        .values(active=False)
    )


def update(
    db: Session,
    bid_attribute_option: BidAttributeOption,
    update_in: BidAttributeOptionUpdate,
):
    db_obj = jsonable_encoder(bid_attribute_option)
    update_obj = update_in.model_dump(exclude_none=True)
    for field in db_obj:
        if field in update_obj:
            setattr(bid_attribute_option, field, update_obj[field])
    db.add(bid_attribute_option)
    return bid_attribute_option


def get_by_value_id(db: Session, type_id: int, value: str):
    return db.scalars(
        select(BidAttributeOption).where(
            (BidAttributeOption.attribute_type_id == type_id)
            & (BidAttributeOption.value == value)
        )
    ).first()


def get(db: Session):
    return db.scalars(
        select(BidAttributeType)
        .options(
            selectinload(
                BidAttributeType.options.and_(BidAttributeOption.active == True)
            )
        )
        .execution_options(populate_existing=True)
    ).all()
