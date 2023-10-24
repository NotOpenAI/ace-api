from sqlmodel import SQLModel, create_engine, Session

from core.config import settings
from db.tables.transactions import Transaction

engine = create_engine(
    url=settings.sync_database_url,
    echo=settings.db_echo_log,
)


def create_transaction():
    transaction = Transaction(amount=10, description="First transaction")

    with Session(engine) as session:
        session.add(transaction)
        session.commit()


def create_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)