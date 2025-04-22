from sqlmodel import Field, SQLModel


class ResourceBaseMixin(SQLModel):
    description: str | None = None


# ORM & Public
class OwnershipMixin(SQLModel):
    # Owner relationship: Many-to-One
    owner_id: str = Field(
        index=True,
        foreign_key="account.id",
        nullable=True,  # allow null
        ondelete="CASCADE",  # when account delete, delete the resource as well
    )
