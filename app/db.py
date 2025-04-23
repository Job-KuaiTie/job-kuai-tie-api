from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import settings

connect_args = {}

# In SQLAlchemy, check_same_thread is a SQLite-specific setting:
if settings.db_type == "sqlite":
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.db_url,
    connect_args=connect_args,
    pool_size=2,
    max_overflow=0,
    pool_recycle=1800,
    pool_pre_ping=True,
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
