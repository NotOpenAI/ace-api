# from schemas.customer import Customer, CustomerCreate
# from sqlalchemy.orm import Session
# from crud.role import create, get_role_by_name, get_all_roles
# from fastapi import APIRouter, Depends, HTTPException
# from core import deps

# router = APIRouter(prefix="/customer",
#     tags=["customer"])

# @router.post("/", response_model=Customer)
# def create_customer(customer_in: CustomerCreate, db: Session = Depends(deps.get_db)):
#     role_exists = get_role_by_name(db, role.name)
#     if role_exists:
#         raise HTTPException(400, "Role already exists")
#     return create(db, role)

# @router.get("/all", response_model=list[Role])
# def get_roles(db: Session = Depends(deps.get_db)):
#     return get_all_roles(db)
