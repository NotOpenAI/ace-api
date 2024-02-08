from sqlalchemy.orm import Session
from schemas.project import ProjectCreateDB, ProjectUpdate
from models.project import Project
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder


def create(db: Session, project: ProjectCreateDB):
    new_project = Project(
        **project.model_dump(),
    )
    db.add(new_project)
    return new_project


def get_by_id(db: Session, id: int):
    return db.scalars(select(Project).where(Project.id == id)).first()


def get(db: Session):
    return db.scalars(select(Project)).all()


def update(db: Session, project: Project, update_in: ProjectUpdate):
    db_obj = jsonable_encoder(project)
    update_obj = update_in.model_dump(exclude_unset=True)
    for field in db_obj:
        if field in update_obj:
            setattr(project, field, update_obj[field])
    db.add(project)
    return project
