from sqlalchemy.orm import Session
from schemas.customer import CustomerCreate
from models.customer import Customer


def create(db: Session, customer: CustomerCreate):
    customer_obj = Customer(**customer.model_dump())
    db.add(customer_obj)
    db.commit()
    db.refresh(customer_obj)
    return customer_obj


def get_by_name(db: Session, name: str):
    return db.query(Customer).filter(Customer.name == name).first()
