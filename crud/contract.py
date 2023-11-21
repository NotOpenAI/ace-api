from sqlalchemy.orm import Session
from schemas.contract import ContractCreate
from models.lookup.contract import Contract
from sqlalchemy import select


def create(db: Session, contract_type: ContractCreate):
    contract = Contract(name=contract_type.name)
    db.add(contract)
    return contract


def get_all_contract_types(db: Session):
    return db.scalars(select(Contract)).all()
