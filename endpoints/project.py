from sqlalchemy.orm import Session
from crud import bid, project
from fastapi import APIRouter, Depends, HTTPException
from core import deps, security
from schemas.base import SuccessResponse
from schemas.bid import BidFull, ProjectUpdate, Bid
from typing import Annotated
from models.user import User


router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/{project_id}", response_model=SuccessResponse[BidFull])
async def get_project(
    project_id: int,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Project Manager"):
        raise HTTPException(401, "Only project managers can get projects")
    db_project = project.get_by_id(db, project_id)
    if not db_project:
        raise HTTPException(404, "Project not found")
    return SuccessResponse(data=db_project)


@router.get("", response_model=SuccessResponse[list[Bid]])
async def get_projects(
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Project Manager"):
        raise HTTPException(401, "Only project managers can get projects")
    return SuccessResponse(data=project.get(db))


@router.put("/{bid_id}", response_model=SuccessResponse[BidFull])
async def update_project(
    bid_id: int,
    project_update: ProjectUpdate,
    current_user: Annotated[User, Depends(security.get_current_user)],
    db: Session = Depends(deps.get_db),
):
    if not current_user.has_role("Project Manager"):
        raise HTTPException(401, "Only project managers can update projects")
    db_project = bid.get_by_id(db, bid_id)
    if not db_project:
        raise HTTPException(404, "Project not found")
    if not any(pm.id == current_user.id for pm in db_project.project_managers):
        raise HTTPException(401, "You do not have permission to manage this project")
    updated_project = project.update(db, db_project, project_update)
    db.commit()
    db.refresh(updated_project)
    return SuccessResponse(data=updated_project)
