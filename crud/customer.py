from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from schemas.customer import CustomerCreate, CustomerUpdate
from models.customer import Customer
from models.customer_contact import CustomerContact
from sqlalchemy import select


def create(db: Session, customer: CustomerCreate):
    customer_obj = Customer(
        name=customer.name,
        phone=customer.phone,
        address=customer.address,
        owner=customer.owner,
        market=customer.market,
        reputation=customer.reputation,
        fin_health=customer.fin_health,
        contacts=[
            CustomerContact(**contact.model_dump()) for contact in customer.contacts
        ],
    )
    db.add(customer_obj)
    return customer_obj


def update(db: Session, customer: Customer, update_in: CustomerUpdate):
    db_obj = jsonable_encoder(customer)
    update_obj = update_in.model_dump(exclude_unset=True)

    for field in db_obj:
        if field in update_obj:
            setattr(customer, field, update_obj[field])

    db.add(customer)
    return customer


def get_by_name(db: Session, name: str):
    return db.scalars(select(Customer).where(Customer.name == name)).first()


def get_all_customers(db: Session):
    return db.scalars(select(Customer)).all()


def get_by_id(db: Session, id: int):
    return db.scalars(select(Customer).where(Customer.id == id)).first()
