from sqlmodel import Field, Relationship
from .base import EntityBase, EntityMixin, EntityPublicMixin, EntityUpdateMixin
from pydantic import EmailStr


class AccountBase(EntityBase):
    email: str = Field(index=True, unique=True)


class Account(EntityMixin, AccountBase, table=True):
    password_hash: str

    # ownership
    companies: list["Company"] = Relationship(back_populates="owner")  # noqa: F821
    jobs: list["Job"] = Relationship(back_populates="owner")  # noqa: F821
    categories: list["Category"] = Relationship(back_populates="owner")  # noqa: F821


class AccountPublic(EntityPublicMixin, AccountBase):
    pass


class AccountCreate(AccountBase):
    password: str
    email: EmailStr = Field(index=True)


class AccountUpdate(EntityUpdateMixin, AccountBase):
    email: EmailStr | None = None
    password: str | None = None
