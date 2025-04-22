from sqlmodel import Relationship
from .base import EntityBase, EntityMixin, EntityPublicMixin, EntityUpdateMixin
from .mixin import ResourceBaseMixin, OwnershipMixin
from typing import Optional
from pydantic import HttpUrl


class CompanyBase(EntityBase, ResourceBaseMixin):
    url: str | None = None
    size: int | None = None


class Company(EntityMixin, CompanyBase, OwnershipMixin, table=True):
    # Refer to owner
    owner: Optional["Account"] = Relationship(back_populates="companies")  # noqa: F821

    # relationship
    jobs: list["Job"] = Relationship(back_populates="company")  # noqa: F821


class CompanyPublic(EntityPublicMixin, CompanyBase, OwnershipMixin):
    pass


class CompanyCreate(CompanyBase):
    url: HttpUrl | None = None


class CompanyUpdate(EntityUpdateMixin, CompanyBase):
    url: HttpUrl | None = None
