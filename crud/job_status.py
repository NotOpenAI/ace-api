from sqlalchemy.orm import Session
from models.lookup.job_status import JobStatus
from schemas.job_status import JobStatusCreate


def create(db: Session, job_status_in: JobStatusCreate):
    job_status = JobStatus(**job_status_in.model_dump())
    db.add(job_status)
    return job_status
