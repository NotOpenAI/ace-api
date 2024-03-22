from sqlalchemy.orm import Session
from schemas.role import RoleCreate
from models.lookup.role import Role
from sqlalchemy import select


def create(db: Session, role: RoleCreate):
    role_obj = Role(**role.model_dump())
    db.add(role_obj)
    return role_obj


def get_role_by_name(db: Session, name: str):
    return db.scalars(select(Role).where(Role.name.ilike(name))).first()


def get_roles_by_ids(db: Session, role_ids: set[int]):
    return db.scalars(select(Role).where(Role.id.in_(role_ids))).all()


def get_all_roles(db: Session):
    return db.scalars(select(Role)).all()
