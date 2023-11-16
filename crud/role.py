from sqlalchemy.orm import Session
from schemas.role import RoleCreate
from models.lookup.role import Role


def create(db: Session, role: RoleCreate):
    role_obj = Role(name=role.name)
    db.add(role_obj)
    db.commit()
    db.refresh(role_obj)
    return role_obj


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def get_roles_by_ids(db: Session, role_ids: set[int]):
    return db.query(Role).filter(Role.id.in_(role_ids)).all()


def get_all_roles(db: Session):
    return db.query(Role).all()
