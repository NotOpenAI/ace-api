from sqlalchemy.orm import Session
from models.lookup.bid_status import BidStatus
from schemas.bid_status import BidStatusCreate


def create(db: Session, bid_status_in: BidStatusCreate):
    bid_status = BidStatus(**bid_status_in.model_dump())
    db.add(bid_status)
    return bid_status
