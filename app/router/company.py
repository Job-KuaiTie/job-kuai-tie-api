from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.db import SessionDep
from app.model import Company, CompanyCreate, CompanyPublic, CompanyUpdate
from app.security import CurrentAccountDep

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.post("/", response_model=CompanyPublic)
def create_company(
    company: CompanyCreate, session: SessionDep, current_account: CurrentAccountDep
):
    # HttpUrl would failed here
    # db_company = Company.model_validate(company)
    db_company = Company(
        **company.model_dump(exclude_unset=True, exclude={"url"}),
        url=str(company.url) if company.url else None,
    )
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company


@router.get("/", response_model=list[CompanyPublic])
def read_companies(
    session: SessionDep,
    current_account: CurrentAccountDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Company]:
    companies = session.exec(select(Company).offset(offset).limit(limit)).all()
    return companies


@router.get("/{company_id}", response_model=CompanyPublic)
def read_company(company_id: str, session: SessionDep) -> Company:
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.patch("/{company_id}", response_model=CompanyPublic)
def update_company(
    company_id: str,
    company: CompanyUpdate,
    session: SessionDep,
    current_account: CurrentAccountDep,
):
    company_db = session.get(Company, company_id)
    if not company_db:
        raise HTTPException(status_code=404, detail="Company not found")
    company_data = company.model_dump(exclude_unset=True)

    # PydanticDeprecatedSince211: Accessing the 'model_fields' attribute on the instance is deprecated.
    # Instead, you should access this attribute from the model class.
    # Deprecated in Pydantic V2.11 to be removed in V3.0.
    # company_db.sqlmodel_update(company_data)

    for key, value in company_data.items():
        setattr(company_db, key, value)

    session.add(company_db)
    session.commit()
    session.refresh(company_db)
    return company_db


@router.delete("/{company_id}")
def delete_company(
    company_id: str, session: SessionDep, current_account: CurrentAccountDep
):
    company = session.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    session.delete(company)
    session.commit()
    return {"ok": True}
