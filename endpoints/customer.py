from schemas.customer import Customer, CustomerCreate, CustomerUpdate, CustomerFull
from sqlalchemy.orm import Session
from crud import customer as customer_crud, customer_contact
from fastapi import APIRouter, Depends, HTTPException
from core import deps, security
from schemas.customer_contact import CustomerContactCreateDB
from schemas.base import SuccessResponse
from typing import Annotated
from models.user import User


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=SuccessResponse[CustomerFull])
def create_customer(
    customer: CustomerCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    try:
        with db.begin_nested():
            new_customer = customer_crud.create(db, customer)
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, str(e))
    db.refresh(new_customer)
    return SuccessResponse(data=new_customer)


@router.put("/{customer_id}", response_model=SuccessResponse[CustomerFull])
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    db_customer = customer_crud.get_by_id(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    try:
        with db.begin_nested():
            updated_customer = customer_crud.update(db, db_customer, customer)

            # Update customer contacts
            if customer.contacts:
                customer_contact.bulk_remove(db, customer_id)
                customer_contact.bulk_create(
                    db,
                    [
                        CustomerContactCreateDB(
                            customer_id=customer_id, **contact.model_dump()
                        )
                        for contact in customer.contacts
                    ],
                )
            db.commit()
        db.refresh(updated_customer)
        return SuccessResponse(data=updated_customer)
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(500, "Internal Server Error")


@router.get("/{id}", response_model=SuccessResponse[CustomerFull])
def get_customer(
    id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    return SuccessResponse(data=customer_crud.get_by_id(db, id))


@router.get("", response_model=SuccessResponse[list[Customer]])
def get_customers(
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    return SuccessResponse(data=customer_crud.get_all(db))
