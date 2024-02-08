from sqlalchemy.orm import Session
from crud import bid, project
from fastapi import APIRouter, Depends, HTTPException
from core import deps
from schemas.base import SuccessResponse
from schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectFull,
    ProjectCreateDB,
    Project,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=SuccessResponse[ProjectFull])
async def create_project(project_in: ProjectCreate, db: Session = Depends(deps.get_db)):
    valid_bid = bid.get_by_id(project_in.bid_id, db)

    if not valid_bid or (valid_bid and not valid_bid.approved):
        raise HTTPException(404, "Cannot create project without approved bid proposal")

    new_project = project.create(
        db,
        ProjectCreateDB(**project_in.model_dump(), customer_id=valid_bid.customer_id),
    )
    db.commit()
    db.refresh(new_project)
    return SuccessResponse(data=new_project)


@router.get("/{project_id}", response_model=SuccessResponse[ProjectFull])
async def get_project(project_id: int, db: Session = Depends(deps.get_db)):
    db_project = project.get_by_id(db, project_id)
    if not db_project:
        raise HTTPException(404, "Project not found")
    return SuccessResponse(data=db_project)


@router.get("", response_model=SuccessResponse[list[Project]])
async def get_projects(db: Session = Depends(deps.get_db)):
    return SuccessResponse(data=project.get(db))


@router.put("/{project_id}", response_model=SuccessResponse[ProjectFull])
async def update_project(
    project_id: int, project_in: ProjectUpdate, db: Session = Depends(deps.get_db)
):
    db_project = project.get_by_id(db, project_id)
    if not db_project:
        raise HTTPException(404, "Project not found")
    # TODO: Add validation so some fields can't be updated after project has been completed(ex: expenses, foreman)
    updated_project = project.update(db, db_project, project_in)
    db.commit()
    db.refresh(updated_project)
    return SuccessResponse(data=updated_project)
