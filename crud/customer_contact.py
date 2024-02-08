from sqlalchemy.orm import Session
from schemas.customer_contact import CustomerContactCreateDB
from models.customer_contact import CustomerContact
from sqlalchemy import select, delete


def bulk_create(db: Session, contacts: list[CustomerContactCreateDB]):
    customer_contact_models = [
        CustomerContact(**contact.model_dump()) for contact in contacts
    ]

    db.add_all(customer_contact_models)
    return customer_contact_models


def bulk_remove(db: Session, customer_id: int):
    db.execute(
        delete(CustomerContact).where(CustomerContact.customer_id == customer_id)
    )


def get_customer_contacts(db: Session, customer_id: int):
    return db.scalars(
        select(CustomerContact).where(CustomerContact.customer_id == customer_id)
    ).all()
