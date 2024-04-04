from schemas.role import Role, RoleCreate
from sqlalchemy.orm import Session
from crud import role
from fastapi import APIRouter, Depends, HTTPException
from core import deps, security
from schemas.base import SuccessResponse
from typing import Annotated
from models.user import User

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("", response_model=SuccessResponse[Role])
def create_role(
    role_in: RoleCreate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Admin"):
        raise HTTPException(401, "Only admins can create roles")
    role_exists = role.get_role_by_name(db, role_in.name)
    if role_exists:
        raise HTTPException(400, "Role already exists")
    new_role = role.create(db, role_in)
    db.commit()
    db.refresh(new_role)
    return SuccessResponse(data=new_role)


@router.get("", response_model=SuccessResponse[list[Role]])
def get_roles(
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Admin"):
        raise HTTPException(401, "Only admins access role list")
    return SuccessResponse(data=role.get_all_roles(db))
