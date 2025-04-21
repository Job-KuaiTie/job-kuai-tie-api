from sqlmodel import Field, SQLModel
from datetime import datetime
from nanoid import generate


def generate_nanoid():
    return generate(size=13)  # Customize size if needed


# Post
class EntityBase(SQLModel):
    name: str = Field(index=True)


# In database
class EntityMixin(EntityBase):
    id: str | None = Field(default_factory=generate_nanoid, primary_key=True)
    created_at: datetime
    updated_at: datetime


# Get
class EntityPublicMixin(EntityBase):
    id: int
    created_at: datetime
    updated_at: datetime


# Patch
class EntityUpdateMixin(EntityBase):
    name: str | None = None
