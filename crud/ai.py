from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from models.bid import Bid
from models.bid_attribute import BidAttribute


def get_bid_data_for_prediction(db: Session):
    # Query to load bids and their attributes including the types
    query = select(Bid).options(
        joinedload(Bid.attributes).joinedload(BidAttribute.type),
    )
    results = db.scalars(query).unique().all()
    return results
