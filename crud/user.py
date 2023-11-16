from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from models.user import User
from core.security import get_password_hash
from fastapi.encoders import jsonable_encoder


def create(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_obj = User(
        username=user.username,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def update(db: Session, user: User, update_in: UserUpdate):
    # convert to dictionary
    db_obj = jsonable_encoder(user)
    update_obj = update_in.model_dump(exclude_unset=True)

    for field in db_obj:
        if field in update_obj:
            setattr(user, field, update_obj[field])

    # make sure password is hashed before updating
    if update_obj["password"]:
        hashed_password = get_password_hash(update_obj["password"])
        setattr(user, "password", hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
