from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate
from models.user import User
from models.user_role import UserRole
from core.security import get_password_hash
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from typing import Optional, List


def create(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_obj = User(
        username=user.username,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role_associations=[UserRole(role_id=role) for role in user.role_ids],
    )

    db.add(user_obj)
    return user_obj


def get_by_id(db: Session, user_id: int):
    return db.scalars(select(User).where(User.id == user_id)).first()


def get_by_username(db: Session, username: str, role_id: Optional[int] = None):
    query = select(User).where(User.username.ilike(username))
    if role_id:
        query = query.where(User.role_associations.any(UserRole.role_id == role_id))
    return db.scalars(query).first()


def get_by_name(db: Session, first_name: str, last_name: str):
    query = (
        select(User)
        .where(User.first_name.ilike(first_name))
        .where(User.last_name.ilike(last_name))
    )
    return db.scalars(query).first()


def get_all(
    db: Session,
    user_ids: Optional[List[int]] = None,
    username: Optional[str] = None,
    role_id: Optional[int] = None,
):
    stmt = select(User)

    if user_ids:
        stmt = stmt.where(User.id.in_(user_ids))
    if username:
        stmt = stmt.where(User.username.icontains(username))
    if role_id:
        stmt = stmt.where(User.role_associations.any(UserRole.role_id == role_id))
    return db.scalars(stmt).all()


def update(db: Session, user: User, update_in: UserUpdate):
    # convert to dictionary
    db_obj = jsonable_encoder(user)
    update_obj = update_in.model_dump(exclude_unset=True)

    for field in db_obj:
        if field in update_obj:
            # hash password before saving in db
            if field == "password":
                hashed_password = get_password_hash(update_obj["password"])
                setattr(user, "hashed_password", hashed_password)
                continue

            # otherwise just update in db
            setattr(user, field, update_obj[field])

    db.add(user)
    return user
