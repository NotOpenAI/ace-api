from schemas.role import Role, RoleCreate
from sqlalchemy.orm import Session
from crud import role
from fastapi import APIRouter, Depends, HTTPException
from core import deps

router = APIRouter(prefix="/role", tags=["role"])


@router.post("/", response_model=Role)
def create_role(role_in: RoleCreate, db: Session = Depends(deps.get_db)):
    role_exists = role.get_role_by_name(db, role_in.name)
    if role_exists:
        raise HTTPException(400, "Role already exists")
    new_role = role.create(db, role_in)
    db.commit()
    db.refresh(new_role)
    return new_role


@router.get("/all", response_model=list[Role])
def get_roles(db: Session = Depends(deps.get_db)):
    return role.get_all_roles(db)
