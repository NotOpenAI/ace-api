from schemas.customer import Customer, CustomerCreate, CustomerUpdate
from sqlalchemy.orm import Session
from crud import customer as customer_crud
from fastapi import APIRouter, Depends, HTTPException
from core import deps

router = APIRouter(prefix="/customer", tags=["customer"])


@router.post("/", response_model=Customer)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(deps.get_db),
):
    try:
        with db.begin_nested():
            new_customer = customer_crud.create(db, customer)
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
    db.refresh(new_customer)
    return new_customer


@router.put("/", response_model=Customer)
def update_customer(
    customer_id: int, customer: CustomerUpdate, db: Session = Depends(deps.get_db)
):
    db_customer = customer_crud.get_by_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer_crud.update(db, db_customer, customer)


@router.get("/", response_model=Customer)
def get_customer(customer_id: int, db: Session = Depends(deps.get_db)):
    return customer_crud.get_by_id(db, customer_id)


@router.get("/list", response_model=list[Customer])
async def get_customer_list(db: Session = Depends(deps.get_db)):
    return customer_crud.get_all_customers(db)
