from sqlalchemy.orm import Session
from sqlalchemy import insert, delete
from schemas.user_role import UserRoleCreate
from models.user_role import UserRole
from crud.user import get_by_id


def bulk_create(db: Session, user_roles: list[UserRoleCreate]):
    user_roles_dict = [user_role.model_dump() for user_role in user_roles]

    roles = db.scalars(insert(UserRole).returning(UserRole), user_roles_dict).all()
    db.commit()
    return roles


def bulk_remove(db: Session, user_id: int):
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    db.scalars(
        delete(UserRole).returning(UserRole).where(UserRole.user_id == user_id)
    ).all()
    db.commit()
    return user_roles
