from sqlmodel import Field, Relationship
from .base import EntityBase, EntityMixin, EntityPublicMixin, EntityUpdateMixin
from .mixin import ResourceBaseMixin, OwnershipMixin
from datetime import datetime
from .job_category import JobCategoryLink
from typing import Optional
from pydantic import HttpUrl
from enum import IntEnum


class JobTier(IntEnum):
    DREAM = 1
    TARGET = 2
    BACKUP = 3


class JobBase(EntityBase, ResourceBaseMixin):
    applied_at: datetime | None = None
    url: str | None = None
    tier: int
    min_yearly_salary: int | None = None
    max_yearly_salary: int | None = None
    # Company relationship (Many-to-One): A job belongs to one company
    company_id: str | None = Field(
        index=True,
        default=None,
        foreign_key="company.id",
        nullable=True,  # allow null
        ondelete="SET NULL",  # on delete would be null
    )


class Job(EntityMixin, JobBase, OwnershipMixin, table=True):
    # Owner relationship (One-to-Many): Account could own many jobs
    owner: Optional["Account"] = Relationship(back_populates="jobs")  # noqa: F821
    company: Optional["Company"] = Relationship(back_populates="jobs")  # noqa: F821

    # Category relationship (Many-to-Many): Jobs can have many categories and vice versa
    categories: list["Category"] = Relationship(  # noqa: F821
        back_populates="jobs", link_model=JobCategoryLink
    )


class JobPublic(EntityPublicMixin, OwnershipMixin, JobBase):
    pass


class JobCreate(JobBase):
    # When create, validate url and tier
    url: HttpUrl | None = None
    tier: JobTier


class JobUpdate(EntityUpdateMixin, JobBase):
    # When update, validate url and tier
    url: HttpUrl | None = None
    tier: JobTier | None = None
