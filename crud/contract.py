from sqlalchemy.orm import Session
from schemas.contract import ContractCreate
from models.lookup.contract import Contract
from sqlalchemy import select


def create(db: Session, contract_type: ContractCreate):
    contract = Contract(**contract_type.model_dump())
    db.add(contract)
    return contract


def get(db: Session):
    return db.scalars(select(Contract)).all()
