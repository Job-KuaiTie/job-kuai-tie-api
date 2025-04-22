from sqlmodel import Field, SQLModel
from datetime import datetime, timezone
from nanoid import generate


def generate_nanoid():
    return generate(size=13)  # Customize size if needed


# Post
class EntityBase(SQLModel):
    name: str = Field(index=True)


# In database
class EntityMixin(EntityBase):
    id: str | None = Field(default_factory=generate_nanoid, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


# Get
class EntityPublicMixin(EntityBase):
    id: str
    created_at: datetime
    updated_at: datetime


# Patch
class EntityUpdateMixin(EntityBase):
    name: str | None = None
