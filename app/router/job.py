from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import SessionDep
from app.model import Job, JobCreate, JobPublic, JobUpdate

router = APIRouter()


@router.post("/jobs/", response_model=JobPublic)
def create_job(job: JobCreate, session: SessionDep):
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


@router.get("/jobs/", response_model=list[JobPublic])
def read_jobs(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Job]:
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs


@router.get("/jobs/{job_id}", response_model=JobPublic)
def read_job(job_id: str, session: SessionDep) -> Job:
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.patch("/jobs/{job_id}", response_model=JobPublic)
def update_job(job_id: str, job: JobUpdate, session: SessionDep):
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


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str, session: SessionDep):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    session.delete(job)
    session.commit()
    return {"ok": True}


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# app = FastAPI()


# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


# class CommonHeaders(BaseModel):
#     host: str
#     save_data: bool
#     if_modified_since: str | None = None
#     traceparent: str | None = None
#     x_tag: list[str] = []


# @router.get("/header_demo/")
# async def header_demo(headers: Annotated[CommonHeaders, Header()]):
#     return headers


# @router.get("/")
# async def root():
#     return {"message": "Hello World"}


# @router.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


# @router.get("/items_with_return/")
# async def read_items_with_return() -> list[Item]:
#     return [
#         Item(name="Portal Gun", price=42.0),
#         Item(name="Plumbus", price=32.0),
#     ]


# @router.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}


# @router.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}


# @router.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}


# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# # @router.get("/items/")
# # async def read_item(skip: int = 0, limit: int = 10):
# #     return fake_items_db[skip : skip + limit]


# @router.get("/items/")
# async def read_items(
#     q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @router.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
