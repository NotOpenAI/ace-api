from sqlalchemy.orm import Session
from sqlalchemy import insert, delete
from schemas.user_role import UserRoleCreate
from models.user_role import UserRole


def bulk_create(db: Session, user_roles: list[UserRoleCreate]):
    user_role_models = [UserRole(**user_role.model_dump()) for user_role in user_roles]
    db.add_all(user_role_models)
    return user_role_models


def bulk_remove(db: Session, user_id: int):
    db.execute(delete(UserRole).where(UserRole.user_id == user_id))
