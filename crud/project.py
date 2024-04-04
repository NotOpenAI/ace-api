from sqlalchemy.orm import Session
from schemas.bid import ProjectUpdate
from models.bid import Bid
from models.project_manager import ProjectManager
from sqlalchemy import select, delete
from fastapi.encoders import jsonable_encoder


def get_by_id(db: Session, id: int):
    query = select(Bid).where(Bid.id == id).where(len(Bid.project_managers) > 0)
    return db.scalars(query).first()


def get(db: Session):
    return db.scalars(select(Bid).where(len(Bid.project_managers) > 0)).all()


def update(db: Session, project: Bid, update_in: ProjectUpdate):
    db_obj = jsonable_encoder(project)
    update_obj = update_in.model_dump(exclude_unset=True)
    for field in db_obj:
        if field in update_obj:
            setattr(project, field, update_obj[field])
    if update_in.project_manager_ids:
        db.execute(
            delete(ProjectManager).where(ProjectManager.project_id == project.id)
        )
        setattr(
            project,
            "pm_associations",
            [ProjectManager(manager_id=id) for id in update_in.project_manager_ids],
        )
    db.add(project)
    return project
