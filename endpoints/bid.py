from sqlalchemy.orm import Session
from crud import contract
from fastapi import APIRouter, Depends, HTTPException
from core import deps
from schemas.contract import Contract, ContractCreate

router = APIRouter(prefix="/bid", tags=["bid"])


@router.post("/contract", response_model=Contract)
def create_bid_contract_type(
    contract_in: ContractCreate, db: Session = Depends(deps.get_db)
):
    new_contract_type = contract.create(db, contract_in)
    db.commit()
    db.refresh(new_contract_type)
    return new_contract_type


@router.get("/contract/all", response_model=list[Contract])
def get_roles(db: Session = Depends(deps.get_db)):
    return contract.get_all_contract_types(db)
