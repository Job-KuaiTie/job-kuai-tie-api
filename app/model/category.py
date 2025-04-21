from sqlmodel import Relationship, Field
from .base import EntityBase, EntityMixin, EntityPublicMixin, EntityUpdateMixin
from .mixin import ResourceBaseMixin
from .job_category import JobCategoryLink
from typing import Optional, Annotated
from pydantic import StringConstraints

# Only allow #RGB or #RRGGBB
HexColorStr = Annotated[
    str,
    StringConstraints(
        pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
        strip_whitespace=True,
        to_upper=True,
    ),
]


class CategoryBase(EntityBase, ResourceBaseMixin):
    color: str = Field(max_length=7)  # e.g., "#FF5733"


class Category(EntityMixin, CategoryBase, table=True):
    # Refer to owner
    owner: Optional["Account"] = Relationship(back_populates="categories")  # noqa: F821

    # Category relationship: Many-to-Many
    jobs: list["Job"] = Relationship(  # noqa: F821
        back_populates="categories", link_model=JobCategoryLink
    )


class CategoryPublic(EntityPublicMixin, CategoryBase):
    pass


class CategoryCreate(CategoryBase):
    # When create, validate the color input
    color: HexColorStr


class CategoryUpdate(EntityUpdateMixin, CategoryBase):
    # When update, validate the color input
    color: HexColorStr | None = None
