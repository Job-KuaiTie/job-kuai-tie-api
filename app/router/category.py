from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import SessionDep
from app.model import Category, CategoryCreate, CategoryPublic, CategoryUpdate
from app.security import CurrentAccountDep

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.post("/", response_model=CategoryPublic)
def create_category(
    category: CategoryCreate, session: SessionDep, current_account: CurrentAccountDep
):
    db_category = Category(
        **category.model_dump(exclude_unset=True, exclude={"url"}),
        owner_id=current_account.id,
    )
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.get("/", response_model=list[CategoryPublic])
def read_categories(
    session: SessionDep,
    current_account: CurrentAccountDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Category]:
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories


@router.get("/{category_id}", response_model=CategoryPublic)
def read_category(
    category_id: str, session: SessionDep, current_account: CurrentAccountDep
) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=CategoryPublic)
def update_category(
    category_id: str,
    category: CategoryUpdate,
    session: SessionDep,
    current_account: CurrentAccountDep,
):
    category_db = session.get(Category, category_id)
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.model_dump(exclude_unset=True)

    # PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated.
    # Instead, you should access this attribute from the model class.
    # Deprecated in Pydantic V2.11 to be removed in V3.0.
    # category_db.sqlmodel_update(category_data)

    for key, value in category_data.items():
        setattr(category_db, key, value)

    session.add(category_db)
    session.commit()
    session.refresh(category_db)
    return category_db


@router.delete("/{category_id}")
def delete_category(
    category_id: str, session: SessionDep, current_account: CurrentAccountDep
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}
