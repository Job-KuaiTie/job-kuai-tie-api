from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import SessionDep
from app.model import Job, JobCreate, JobPublic, JobUpdate
from app.security import CurrentAccountDep

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.post("/", response_model=JobPublic)
def create_job(job: JobCreate, session: SessionDep, current_account: CurrentAccountDep):
    # HttpUrl would failed here
    # db_job = Job.model_validate(job)
    db_job = Job(
        **job.model_dump(exclude_unset=True, exclude={"url"}),
        url=str(job.url) if job.url else None,
    )
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job


@router.get("/", response_model=list[JobPublic])
def read_jobs(
    session: SessionDep,
    current_account: CurrentAccountDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs


@router.get("/{job_id}", response_model=JobPublic)
def read_job(
    job_id: str, session: SessionDep, current_account: CurrentAccountDep
) -> Job:
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.patch("/{job_id}", response_model=JobPublic)
def update_job(
    job_id: str, job: JobUpdate, session: SessionDep, current_account: CurrentAccountDep
):
    job_db = session.get(Job, job_id)
    if not job_db:
        raise HTTPException(status_code=404, detail="Job not found")
    job_data = job.model_dump(exclude_unset=True)

    # PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated.
    # Instead, you should access this attribute from the model class.
    # Deprecated in Pydantic V2.11 to be removed in V3.0.
    # job_db.sqlmodel_update(job_data)

    for key, value in job_data.items():
        setattr(job_db, key, value)

    session.add(job_db)
    session.commit()
    session.refresh(job_db)
    return job_db


@router.delete("/{job_id}")
def delete_job(job_id: str, session: SessionDep, current_account: CurrentAccountDep):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    session.delete(job)
    session.commit()
    return {"ok": True}
