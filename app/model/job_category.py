from sqlmodel import SQLModel, Field


class JobCategoryLink(SQLModel, table=True):
    job_id: str | None = Field(
        default=None,
        foreign_key="job.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    category_id: str | None = Field(
        default=None,
        foreign_key="category.id",
        primary_key=True,
        ondelete="CASCADE",
    )
